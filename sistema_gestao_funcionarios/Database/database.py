import sqlite3
import os
from typing import List, Tuple, Optional
import time
import shutil
from datetime import datetime

# Caminho absoluto para o banco (fica na raiz do projeto, junto com main.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "DB_Gestao_Funcionarios.db")

# Simple in-memory cache for cargos to avoid frequent DB hits; invalidated on writes
_cargos_cache: Optional[List[str]] = None
_cargos_cache_timestamp: Optional[float] = None
_CARGOS_CACHE_TTL = 5.0  # seconds - short TTL to keep cache fresh but reduce queries



def _get_connection() -> sqlite3.Connection:
    """Cria uma conexão configurada para uso da aplicação.

    - row_factory retorna rows acessíveis por índice e por nome quando útil
    - habilita foreign_keys e define journal_mode=WAL para melhor concorrência
    - check_same_thread=False para permitir acesso em threads diferentes (UI -> background)
    """
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Pragmas recomendadas para aplicações desktop/pequeno servidor com SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def inicializar_banco() -> None:
    """Cria as tabelas e índices necessários (idempotente)."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                genero TEXT,
                cargo TEXT,
                email TEXT,
                salario REAL
            )
            """
        )
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_funcionarios_nome ON funcionarios(nome)")
        conn.commit()


def _invalidate_cargos_cache():
    global _cargos_cache, _cargos_cache_timestamp
    _cargos_cache = None
    _cargos_cache_timestamp = None


def inserir_funcionario(dados: dict) -> int:
    """Insere um funcionário. Retorna o id criado."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO funcionarios (nome, genero, cargo, email, salario)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                dados["nome"],
                dados.get("genero"),
                dados.get("cargo"),
                dados.get("email"),
                float(dados.get("salario", 0.0)),
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
    # Invalidate cache outside connection
    _invalidate_cargos_cache()
    return new_id


def listar_funcionarios(limite: int = 50, offset: int = 0) -> List[Tuple]:
    """Retorna lista de tuplas: (id, nome, genero, cargo, email, salario_fmt)"""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                id,
                nome,
                genero,
                cargo,
                email,
                'R$ ' || printf('%.2f', salario) as salario_fmt
            FROM funcionarios
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limite, offset),
        )
        rows = cursor.fetchall()
        return [tuple(r) for r in rows]


def pesquisar_funcionarios(termo: str = "", cargo: Optional[str] = None, limite: int = 100, offset: int = 0) -> List[Tuple]:
    """Busca por nome, cargo ou e-mail. Quando termo for vazio e cargo fornecido, filtra apenas por cargo.

    Retorna tuplas: (id, nome, genero, cargo, email, salario_fmt)
    """
    with _get_connection() as conn:
        cursor = conn.cursor()
        params = []
        where_clauses = []

        if termo:
            like = f"%{termo}%"
            where_clauses.append("(nome LIKE ? OR cargo LIKE ? OR email LIKE ?)")
            params.extend([like, like, like])

        if cargo and cargo.strip() and cargo != "Todos os cargos":
            # Compare trimmed and lower-cased values for resilient matching (ignore case/whitespace)
            where_clauses.append("LOWER(TRIM(cargo)) = LOWER(TRIM(?))")
            params.append(cargo)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        query = f"""
            SELECT
                id,
                nome,
                genero,
                cargo,
                email,
                'R$ ' || printf('%.2f', salario) as salario_fmt
            FROM funcionarios
            {where_sql}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """
        params.extend([limite, offset])
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [tuple(r) for r in rows]


def listar_cargos() -> List[str]:
    """Retorna uma lista de cargos distintos (strings), ordenada alfabeticamente.

    Usa um cache curto para reduzir acessos ao banco em UIs que atualizam frequentemente.
    """
    global _cargos_cache, _cargos_cache_timestamp
    now = time.time()
    if _cargos_cache is not None and _cargos_cache_timestamp is not None and (now - _cargos_cache_timestamp) < _CARGOS_CACHE_TTL:
        return list(_cargos_cache)

    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT cargo FROM funcionarios WHERE cargo IS NOT NULL AND cargo != '' ORDER BY cargo COLLATE NOCASE ASC")
        rows = cursor.fetchall()
        # Normalize returned cargos by trimming whitespace
        cargos = [r[0].strip() for r in rows if r[0] is not None]

    _cargos_cache = cargos
    _cargos_cache_timestamp = now
    return cargos


def obter_funcionario_por_id(func_id: int) -> Optional[Tuple]:
    """Retorna uma tupla com os dados brutos de um funcionário (incluindo salario numérico)."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nome, genero, cargo, email, salario
            FROM funcionarios
            WHERE id = ?
            """,
            (func_id,),
        )
        row = cursor.fetchone()
        return tuple(row) if row is not None else None


def atualizar_funcionario(dados: dict) -> None:
    """Atualiza um funcionário existente.

    dados: dict com 'id', 'nome', 'genero', 'cargo', 'email', 'salario'
    """
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE funcionarios
            SET nome = ?, genero = ?, cargo = ?, email = ?, salario = ?
            WHERE id = ?
            """,
            (
                dados["nome"],
                dados.get("genero"),
                dados.get("cargo"),
                dados.get("email"),
                float(dados.get("salario", 0.0)),
                int(dados["id"]),
            ),
        )
        conn.commit()
    # Invalidate cache after update
    _invalidate_cargos_cache()


def excluir_funcionario(func_id: int) -> None:
    """Remove um funcionário pelo ID."""
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE id = ?", (func_id,))
        conn.commit()
    # Invalidate cache after delete
    _invalidate_cargos_cache()


# ========== ESTATÍSTICAS PARA O DASHBOARD ==========

def contar_funcionarios() -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM funcionarios")
        return int(cursor.fetchone()[0] or 0)


def contar_cargos() -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT cargo) FROM funcionarios")
        return int(cursor.fetchone()[0] or 0)


def media_salarial() -> float:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(salario) FROM funcionarios")
        resultado = cursor.fetchone()[0]
        return float(resultado) if resultado is not None else 0.0


def backup_db(backup_dir: Optional[str] = None) -> str:
    """Cria um backup consistente do arquivo SQLite usando a API backup do sqlite3.

    - backup_dir: diretório para salvar o backup. Se None, usa o mesmo diretório do DB.
    - retorna o caminho do arquivo de backup criado.
    """
    src = DB_PATH
    if backup_dir is None:
        backup_dir = os.path.dirname(DB_PATH)
    # nome com timestamp
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    dst = os.path.join(backup_dir, f"DB_Gestao_Funcionarios_backup_{ts}.db")

    # Usa a API backup: cria uma nova conexão para o destino e copia
    dest_conn = sqlite3.connect(dst)
    try:
        with _get_connection() as src_conn:
            src_conn.backup(dest_conn, pages=0, progress=None)
    finally:
        dest_conn.close()

    return dst
