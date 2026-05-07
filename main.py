"""
Sistema de Gestão de Funcionários
Autor: [Bernardo]
Descrição: CRUD completo com persistência de dados em JSON,
desenvolvido inteiramente em ambiente mobile (Pydroid 3).
"""

import os
import time
import json
import random
import sys
from datetime import datetime

ARQUIVO_DADOS = "funcionarios.json"

# --- Classe Funcionário ---

class Funcionario:
    def __init__(self, nome, idade, cargo, genero):
        self.nome = nome
        self.idade = idade
        self.cargo = cargo
        self.genero = genero

    def para_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "cargo": self.cargo,
            "genero": self.genero
        }

    def __str__(self):
        return f"Nome: {self.nome} | Idade: {self.idade} | Cargo: {self.cargo} | Gênero: {self.genero}"

# --- Funções de memória JSON ---

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump([func.para_dict() for func in funcionarios], f, indent=4, ensure_ascii=False)

def carregar_dados():
    global funcionarios
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                funcionarios = [Funcionario(**d) for d in dados]
        except:
            funcionarios = []

# --- Dados globais ---

funcionarios = []
cargos_utilizados = []

dicas = [
    "💡 Insight: Equipes com idades variadas equilibram energia e experiência.",
    "💡 Aviso: Manter o Gênero atualizado ajuda a monitorizar a diversidade.",
    "⚙️ Atalho: Use a pesquisa (Opção 4) para encontrar alguém rapidamente.",
    "⚙️ Aviso: Se o gênero estiver errado, apague e cadastre novamente.",
    "✨ A sua base de dados está a crescer! Continue assim.",
    "✨ Organização é o primeiro passo para o sucesso!",
    "⚙️ Dica: Revise os cargos periodicamente para manter os dados atualizados.",
    "💡 Gestão: Feedbacks construtivos são ferramentas de crescimento, não de crítica.",
    "⚙️ Sistema: Use nomes completos para evitar confusão entre homônimos.",
    "✨ Tudo pronto para mais um dia de boa gestão!"
]

ativar_dicas = False
salvamento_automatico = False
mostrar_generos = False
mostrar_sugestoes = False

# --- Utilitários ---

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def dicas_layout():
    if ativar_dicas:
        print(random.choice(dicas))
        print("=+========-========++++========-=========+=")

def _definir_config(global_name, valor, msg):
    globals()[global_name] = valor
    input(f"{msg} Aperte enter...")

# --- Menu ---

def menu():
    generos = [f.genero for f in funcionarios]
    t_hmns = generos.count("Masculino")
    t_mlrs = generos.count("Feminino")
    t_outros = generos.count("Outro")
    print("-===-💻 • Gestão de funcionários • 💻-====-")
    print("1. Cadastrar funcionário")
    print("2. Deletar funcionário")
    print("3. Listar funcionários")
    print("4. Pesquisar funcionário")
    if not salvamento_automatico:
        print("5. Salve seu projeto!")
    print("6. Sair")
    print("7. Configurações")
    print("8. Gerar relatório")
    if salvamento_automatico:
        print("=+========-========++++========-=========+=")
        print("💾 • Salvamento automático • 💾")
    print("=+========-========++++========-=========+=")
    print(f"⚒️ • Funcionários cadastrados: {len(funcionarios)}")
    print("=+========-========++++========-=========+=")
    if mostrar_generos:
        print("                  Gêneros")
        print("")
        print(f"🧑 Masculino: {t_hmns} 👩 Feminino: {t_mlrs} 🙇 Outro: {t_outros}")
        print("=+========-========++++========-=========+=")

# --- CRUD ---

def cadastrar_funcionario():
    nome = str(input("🏷 Qual o nome do(a) funcionário(a) que deseja cadastrar?\n")).title().strip()
    idade = int(input("🎂 Quantos anos ele(a) tem?\n"))
    if cargos_utilizados and mostrar_sugestoes:
        print("👨‍🏫 Sugestão de cargos já utilizados:")
        print(f" - {cargos_utilizados}")
    cargo = str(input("🛡 Qual o cargo dele(a)?\n")).capitalize().strip()
    if cargo not in cargos_utilizados and mostrar_sugestoes:
        cargos_utilizados.append(cargo)
    genero = str(input("🧑 Qual o gênero dele(a)? M/F/O\n")).upper().strip()

    mapa_genero = {"M": "Masculino", "F": "Feminino", "O": "Outro"}
    if genero not in mapa_genero:
        print("❌️ Erro! Cadastre novamente.")
        time.sleep(1)
        return

    func = Funcionario(nome, idade, cargo, mapa_genero[genero])
    funcionarios.append(func)

    if salvamento_automatico:
        salvar_dados()
        print("💾 Salvo automaticamente!")
    input("✅ Funcionário cadastrado! Aperte enter...")

def apagar_funcionario():
    if not funcionarios:
        print("❌️ Nenhum funcionário para remover!")
        time.sleep(1)
        return

    listar_funcionarios()
    posicao = int(input("⌨️ Digite o número do funcionário que deseja remover, para todos digite 0: "))

    if posicao == 0:
        confirmacao = input("⚠️ Deseja excluir TODOS? S/N? ").upper().strip()
        if confirmacao == 'S':
            funcionarios.clear()
            print("✅️ Todos foram removidos com sucesso!")
        else:
            print("❌️ Nenhum funcionário removido!")
        time.sleep(1)
        return

    if posicao < 1 or posicao > len(funcionarios):
        input("❌️ Esse funcionário não existe! Aperte enter...")
        return

    funcionarios.pop(posicao - 1)
    print(f"✅️ Funcionário {posicao} removido com sucesso!")
    time.sleep(1)

    if salvamento_automatico:
        salvar_dados()
        print("💾 Salvo automaticamente!")

def listar_funcionarios():
    if not funcionarios:
        print("👷‍♂️ Nenhum funcionário cadastrado!")
    else:
        for i, f in enumerate(funcionarios, start=1):
            print(f"{i}º | {f}")

def pesquisar_funcionarios():
    if not funcionarios:
        input("❌️ Nenhum funcionário cadastrado! Pressione enter...")
        return

    busca = input("💻 Digite o nome do funcionário que gostaria de pesquisar: ").title().strip()
    encontrado = False
    print("----------🔎 Resultados da busca 🔍----------")
    for i, f in enumerate(funcionarios, start=1):
        if busca in f.nome:
            print(f"{i}º | {f}")
            print("-------------------------------------------")
            encontrado = True

    if not encontrado:
        print("❌️ Nenhum funcionário encontrado!")
    input("⌨️ Pressione enter para continuar...")

def gerar_relatorio():
    if not funcionarios:
        input("❌️ Nenhum funcionário cadastrado! Aperte enter...")
        return

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    generos = [f.genero for f in funcionarios]

    with open("relatorio.txt", "w", encoding="utf-8") as arq:
        arq.write("========================================\n")
        arq.write("       RELATÓRIO DE FUNCIONÁRIOS        \n")
        arq.write("========================================\n")
        arq.write(f"Gerado em: {agora}\n")
        arq.write(f"Total de funcionários: {len(funcionarios)}\n")
        arq.write(f"Masculino: {generos.count('Masculino')} | Feminino: {generos.count('Feminino')} | Outro: {generos.count('Outro')}\n")
        arq.write("----------------------------------------\n")
        for i, f in enumerate(funcionarios, start=1):
            arq.write(f"{i}º | {f}\n")
        arq.write("========================================\n")

    input("✅ Relatório gerado em 'relatorio.txt'! Aperte enter...")

# --- Configurações ---

acoes_config = {
    "1": lambda: _definir_config("ativar_dicas", True,  "✅ Dicas ativadas!"),
    "2": lambda: _definir_config("ativar_dicas", False, "❌ Dicas desativadas!"),
    "3": lambda: _definir_config("salvamento_automatico", True,  "💾 Salvamento automático ativado!"),
    "4": lambda: _definir_config("salvamento_automatico", False, "❌ Salvamento automático desativado!"),
    "5": lambda: _definir_config("mostrar_generos", True,  "👥 Gêneros ativados!"),
    "6": lambda: _definir_config("mostrar_generos", False, "🙇 Gêneros escondidos!"),
    "7": lambda: _definir_config("mostrar_sugestoes", True,  "💡 Sugestões ativadas!"),
    "8": lambda: _definir_config("mostrar_sugestoes", False, "👷‍♂️ Sugestões escondidas!"),
}

def configuracoes():
    while True:
        limpar_tela()
        print("-====+====- ⚙️ Configurações ⚙️ -====+====-")
        print("1. Ativar dicas")
        print("2. Desativar dicas")
        print("3. Ativar salvamento automático")
        print("4. Desativar salvamento automático")
        print("5. Mostrar gêneros")
        print("6. Esconder gêneros")
        print("7. Mostrar sugestões")
        print("8. Esconder sugestões")
        print("0. Voltar")
        escolha_conf = input("\n👨‍🏭 O que deseja configurar? ")
        if escolha_conf == "0":
            print("↩️ Voltando...")
            time.sleep(1)
            break
        acao = acoes_config.get(escolha_conf)
        if acao:
            acao()
        else:
            input("❌ Opção inválida! Aperte enter...")

# --- Loop principal com dicionário de ações ---

acoes_menu = {
    1: cadastrar_funcionario,
    2: apagar_funcionario,
    3: lambda: (listar_funcionarios(), input("Pressione enter para continuar...\n")),
    4: pesquisar_funcionarios,
    5: lambda: (salvar_dados(), input("✅️ Projeto salvo com sucesso! Aperte enter...")),
    7: configuracoes,
    8: gerar_relatorio,
}

if __name__ == "__main__":
    carregar_dados()
    escolha = 0

    while escolha != 6:
        limpar_tela()
        menu()
        dicas_layout()
        try:
            escolha = int(input("🚀 Digite o número referente a sua escolha:\n"))
        except:
            input("❌️ Nenhuma opção selecionada! Aperte enter...")
            continue

        if escolha == 6:
            print("👋 Saindo...")
            break

        acao = acoes_menu.get(escolha)
        if acao:
            try:
                acao()
            except Exception as e:
                input(f"❌️ Erro! Aperte enter...")
        else:
            input("❌️ Escolha inválida!")
