import customtkinter as ctk
from tkinter import ttk

from Database.database import listar_funcionarios, pesquisar_funcionarios, obter_funcionario_por_id, excluir_funcionario, listar_cargos

# Design tokens
FONT_FAMILY = "Inter"
BG = "#0b1220"
SURFACE = "#0f1724"
MUTED = "#94A3B8"
TEXT = "#E6EEF8"
ACCENT = "#4F46E5"
ACCENT_HOVER = "#4338CA"
SUCCESS = "#10B981"
DANGER = "#EF4444"


class FuncionariosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        self.header.grid_columnconfigure(1, weight=1)

        self.titulo = ctk.CTkLabel(
            self.header,
            text="👤 Funcionários",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo.grid(row=0, column=0, sticky="w")

        self.btn_novo = ctk.CTkButton(
            self.header,
            text="+ Novo funcionário",
            width=160,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.controller.abrir_cadastro()
        )
        self.btn_novo.grid(row=0, column=1, sticky="e")

        # Filtros e pesquisa
        self.filtros_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=SURFACE)
        self.filtros_frame.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        self.filtros_frame.grid_columnconfigure(1, weight=1)

        self.filtro_entry = ctk.CTkEntry(
            self.filtros_frame,
            placeholder_text="🔎 Pesquisar por nome, cargo ou e-mail...",
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13)
        )
        self.filtro_entry.grid(row=0, column=0, padx=15, pady=12, sticky="ew")

        self.filtro_cargo = ctk.CTkOptionMenu(
            self.filtros_frame,
            values=["Todos os cargos"],
            width=200,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13)
        )
        self.filtro_cargo.grid(row=0, column=1, padx=(0, 10), pady=12)

        # Preencher opções de cargos dinamicamente a partir do banco
        try:
            cargos = listar_cargos()
            choices = ["Todos os cargos"] + cargos if cargos else ["Todos os cargos"]
            self.filtro_cargo.configure(values=choices)
            self.filtro_cargo.set(choices[0])
        except Exception:
            # mantém opções padrão já definidas
            pass

        self.filtro_btn = ctk.CTkButton(
            self.filtros_frame,
            text="Filtrar",
            width=120,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.filtrar_demo
        )
        self.filtro_btn.grid(row=0, column=2, padx=(0, 15), pady=12)

        # Tabela
        self.tabela_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e1e2e")
        self.tabela_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.tabela_frame.grid_columnconfigure(0, weight=1)
        self.tabela_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
            background=SURFACE,
            foreground=TEXT,
            fieldbackground=SURFACE,
            borderwidth=0,
            font=(FONT_FAMILY, 11),
            rowheight=36
        )
        style.configure("Treeview.Heading",
            background="#0d1a2a",
            foreground=TEXT,
            font=(FONT_FAMILY, 12, "bold"),
            borderwidth=0
        )
        style.map("Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", TEXT)]
        )

        # Columns: keep only data columns — remove unused 'ações' column to simplify UI
        colunas = ("id", "nome", "genero", "cargo", "email", "salario")
        self.tree = ttk.Treeview(self.tabela_frame, columns=colunas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("genero", text="Gênero")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salario", text="Salário")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=220, anchor="w")
        self.tree.column("genero", width=90, anchor="center")
        self.tree.column("cargo", width=180, anchor="w")
        self.tree.column("email", width=220, anchor="w")
        self.tree.column("salario", width=120, anchor="e")

        self.scrollbar = ctk.CTkScrollbar(self.tabela_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(15, 0), pady=15)
        self.scrollbar.grid(row=0, column=1, sticky="ns", pady=15)

        # Horizontal scrollbar to allow full table visibility in windowed mode
        try:
            self.h_scrollbar = ctk.CTkScrollbar(self.tabela_frame, orientation='horizontal', command=self.tree.xview)
            self.tree.configure(xscrollcommand=self.h_scrollbar.set)
            self.h_scrollbar.grid(row=1, column=0, columnspan=2, sticky='ew', padx=(15,0), pady=(0,10))
        except Exception:
            # fallback: some CTk versions may not support orientation arg; try tk.Scrollbar
            try:
                from tkinter import Scrollbar
                h = Scrollbar(self.tabela_frame, orient='horizontal', command=self.tree.xview)
                self.tree.configure(xscrollcommand=h.set)
                h.grid(row=1, column=0, columnspan=2, sticky='ew', padx=(15,0), pady=(0,10))
            except Exception:
                pass

        # Paginação inicial
        self.current_page = 1
        # aumentar page_size para reduzir número de chamadas ao BD em uso normal
        self.page_size = 25

        # Paginação
        self.paginacao_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paginacao_frame.grid(row=3, column=0, sticky="ew")

        self.btn_anterior = ctk.CTkButton(
            self.paginacao_frame,
            text="← Anterior",
            width=100,
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#2a2a40",
            hover_color="#3a3a55",
            command=self.pagina_anterior
        )
        self.btn_anterior.pack(side="left")

        self.pagina_label = ctk.CTkLabel(
            self.paginacao_frame,
            text="Página 1",
            font=ctk.CTkFont(size=13),
            text_color="#888899"
        )
        self.pagina_label.pack(side="left", padx=20)

        self.btn_proximo = ctk.CTkButton(
            self.paginacao_frame,
            text="Próxima →",
            width=100,
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#2a2a40",
            hover_color="#3a3a55",
            command=self.pagina_proxima
        )
        self.btn_proximo.pack(side="left")

        # Carrega dados após widgets de paginação existirem
        self.carregar_dados()
        # binds para melhorias de usabilidade
        self._bind_keys()

        # Botões de ação da tabela (simulados)
        self.acoes_tabela_frame = ctk.CTkFrame(self.paginacao_frame, fg_color="transparent")
        self.acoes_tabela_frame.pack(side="right")

        self.btn_editar = ctk.CTkButton(
            self.acoes_tabela_frame,
            text="✏️ Editar",
            width=90,
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self.editar_selecionado
        )
        self.btn_editar.pack(side="left", padx=(0, 8))

        self.btn_excluir = ctk.CTkButton(
            self.acoes_tabela_frame,
            text="🗑️ Excluir",
            width=90,
            height=34,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.excluir_selecionado
        )
        self.btn_excluir.pack(side="left")

    def carregar_dados(self):
        """Carrega os dados do banco para a tabela com paginação simples."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        offset = (self.current_page - 1) * self.page_size
        try:
            rows = listar_funcionarios(self.page_size, offset)
        except Exception:
            rows = []

        for row in rows:
            # row já é uma tupla: (id, nome, genero, cargo, email, salario_fmt)
            self.tree.insert("", "end", values=row)

        # Atualiza label de página
        self.pagina_label.configure(text=f"Página {self.current_page}")

    def filtrar_demo(self):
        """Aplica pesquisa usando o banco de dados. Se ambos campos vazios, recarrega a página atual.

        Agora suporta filtragem por termo e por cargo selecionado.
        """
        termo = self.filtro_entry.get().strip()
        cargo = self.filtro_cargo.get() if hasattr(self.filtro_cargo, 'get') else None

        # Se ambos vazios/defaut, recarrega
        if (not termo) and (not cargo or cargo == "Todos os cargos"):
            self.carregar_dados()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rows = pesquisar_funcionarios(termo, cargo, limite=200, offset=0)
        except Exception:
            rows = []

        for row in rows:
            self.tree.insert("", "end", values=row)

        self.pagina_label.configure(text=f"Resultados: {len(rows)}")

    # permitir duplo clique para editar e tecla Delete para excluir
    def _bind_keys(self):
        try:
            # bind double click with event to correctly identify row under cursor
            self.tree.bind("<Double-1>", self._on_double_click)
            self.tree.master.bind_all("<Delete>", lambda e: self.excluir_selecionado())
        except Exception:
            pass

    def _on_double_click(self, event):
        """Handle double-click on treeview row: ensure the clicked row is selected then open editor."""
        try:
            row_id = self.tree.identify_row(event.y)
            if row_id:
                # select the row so editar_selecionado works reliably
                self.tree.selection_set(row_id)
                self.editar_selecionado()
        except Exception:
            # fallback to existing behavior
            try:
                self.editar_selecionado()
            except Exception:
                pass

    def pagina_anterior(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.carregar_dados()

    def pagina_proxima(self):
        # Tenta carregar a próxima página e só avança se houver resultados
        offset = self.current_page * self.page_size
        try:
            rows = listar_funcionarios(self.page_size, offset)
        except Exception:
            rows = []
        if rows:
            self.current_page += 1
            self.carregar_dados()

    def editar_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.mostrar_aviso("Selecione um funcionário para editar.")
            return

        valores = self.tree.item(selecionado[0], "values")
        try:
            func_id = int(valores[0])
        except Exception:
            self.mostrar_aviso("ID inválido selecionado.")
            return

        row = obter_funcionario_por_id(func_id)
        if not row:
            self.mostrar_aviso("Funcionário não encontrado no banco de dados.")
            return

        # row: (id, nome, genero, cargo, email, salario)
        salario_raw = row[5] if row[5] is not None else 0.0
        dados = {
            "id": row[0],
            "nome": row[1],
            "genero": row[2] or "",
            "cargo": row[3] or "",
            "email": row[4] or "",
            # passar salário como string numérica para o formulário
            "salario": f"{float(salario_raw):.2f}"
        }
        self.controller.abrir_cadastro(modo="editar", dados=dados)

    def excluir_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.mostrar_aviso("Selecione um funcionário para excluir.")
            return

        valores = self.tree.item(selecionado[0], "values")
        try:
            func_id = int(valores[0])
        except Exception:
            self.mostrar_aviso("ID inválido selecionado.")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar exclusão")
        dialog.geometry("380x170")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="🗑️ Tem certeza?", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 8))
        ctk.CTkLabel(dialog, text="Deseja remover este funcionário? Esta ação não poderá ser desfeita.", font=ctk.CTkFont(size=12), wraplength=320).pack(pady=(0, 15))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(0, 10))

        def do_excluir():
            try:
                excluir_funcionario(func_id)
                dialog.destroy()
                # recarrega página atual
                self.carregar_dados()
            except Exception as e:
                dialog.destroy()
                self.mostrar_aviso(f"Erro ao excluir: {e}")

        ctk.CTkButton(btn_frame, text="Cancelar", width=100, fg_color="#555566", hover_color="#444455", command=dialog.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Excluir", width=100, fg_color="#ef4444", hover_color="#dc2626", command=do_excluir).pack(side="left", padx=5)

    def mostrar_aviso(self, mensagem, title="Aviso"):
        """Use o helper centralizado do controller quando disponível para mensagens consistentes."""
        try:
            # controller.mostrar_aviso implementa auto-close por padrão
            self.controller.mostrar_aviso(mensagem, title=title)
        except Exception:
            # fallback leve (auto-close curto)
            dlg = ctk.CTkToplevel(self)
            dlg.title(title)
            dlg.geometry('320x110')
            ctk.CTkLabel(dlg, text=mensagem, font=ctk.CTkFont(size=13), wraplength=280).pack(pady=(18, 12))
            dlg.after(2500, dlg.destroy)
