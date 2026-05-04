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

#arquivo onde serão armazenados os dados do usuário

ARQUIVO_DADOS = "funcionarios.json"

# --- Funções de memoria json ---

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(funcionarios, f, indent=4, ensure_ascii=False)

def carregar_dados():
    global funcionarios
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                funcionarios = json.load(f)
        except:
            funcionarios = []

#Lista dos funcionários e dos cargos, o "núcleo" do projeto
funcionarios = []
cargos_utilizados = []

#Dicas meramente ilustrativas que podem ser ativadas nas configurações
dicas = [
        "💡 Insight: Equipes com idades variadas equilibram energia e experiência.",
        "💡 Aviso: Manter o Gênero atualizado ajuda a monitorizar a diversidade.",
        "⚙️ Atalho: Use a pesquisa (Opção 4) para encontrar alguém rapidamente.",
        "⚙️ Aviso: Se o gênero estiver errado, apague e cadastre novamente.",
        "✨: A sua base de dados está a crescer! Continue assim.",
        "✨: Organização é o primeiro passo para o sucesso!",
        "⚙️ Dica: Revise os cargos periodicamente para manter os dados atualizados.",
        "💡 Gestão: Feedbacks construtivos são ferramentas de crescimento, não de crítica.",
        "⚙️ Sistema: Use nomes completos para evitar confusão entre homônimos.",
        "✨: Tudo pronto para mais um dia de boa gestão!"
    ]

#Outras variáveis importantes
escolha = 0
ativar_dicas = False
salvamento_automatico = False
mostrar_generos = False
mostrar_sugestoes = False

#função de menu
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")
    
def apagar_linhas(n=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        
#menu em função                
def menu():
    generos = [f['genero'] for f in funcionarios]
    t_hmns = generos.count("Masculino")
    t_mlrs = generos.count("Feminino")
    t_outros = generos.count("Outro")
    print("-===-💻 • Gestão de funcionários • 💻-====-")
    print("1. Cadastrar funcionário")
    print("2. Deletar funcionário")
    print("3. Listar funcionários")
    print("4. Pesquisar funcionário")
    if salvamento_automatico == False:
        print("5. Salve seu projeto!")
    print("6. Sair")
    print("7. Configurações")
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

#função do layout das dicas
def dicas_layout(quantidade=3):
    if ativar_dicas == True:
        print(random.choice(dicas))
        print("=+========-========++++========-=========+=")

        
#função de cadastrar usuário
def cadastrar_funcionario():
    nome = str(input("🏷 Qual o nome do(a) funcionário(a) que deseja cadastrar?\n")).title().strip()
    idade = int(input("🎂 Quantos anos ele(a) tem?\n"))
    if cargos_utilizados:
        print("👨‍🏫 sugestão de cargos já utilizados:")
        print(f" - {cargos_utilizados}")
    cargo = str(input("🛡 Qual o cargo dele(a)?\n")).capitalize().strip()
    if cargo not in cargos_utilizados and mostrar_sugestoes:
        cargos_utilizados.append(cargo) 
    genero = str(input("🧑 Qual o gênero dele(a)? M/F/O\n")).title().strip()
       
    if genero == "M":
       genero = "Masculino"
    elif genero == "F":
       genero = "Feminino"
    elif genero == "O":
       genero = "Outro" 
    else:
       print("❌️Erro! Cadastre novamente.")
       time.sleep(1)
       return
    funcionario = {
    "nome": nome,
    "idade": idade,
    "cargo": cargo,
    "genero": genero
}
    funcionarios.append(funcionario)
    if salvamento_automatico == True:
       salvar_dados()
       print("💾 Salvo automaticamente!")
    input("✅ funcionário cadastrado! Aperte enter...")

#função de apagar funcionarios utilizando sistema de comparação   

def apagar_funcionario():
    if not funcionarios:
        print("❌️ Nenhum funcionário para remover!")
        time.sleep(1)
    else:
        listar_funcionarios()
        posicao = int(input("⌨️ Digite o número do funcionário que deseja remover, para todos digite 0: "))
        if posicao == 0:
            todos = input("⚠️ Deseja excluir TODOS? S/N?").title().upper().strip()
            if todos == 'S':
                print("✅️ Todos foram removidos com sucesso!")
                funcionarios.clear()
                time.sleep(1)
                return
            elif todos == 'N':
                print("❌️ Nenhum funcionário removido!")
                time.sleep(1)
                return
        if posicao > len(funcionarios) or posicao < 0:
            input("❌️ Esse funcionário não existe! aperte enter...")
            return
        removido = funcionarios.pop(posicao - 1)
        print(f"✅️ Funcionário {posicao} removido com sucesso!")
        time.sleep(1)
        if salvamento_automatico:
           salvar_dados()
           print("💾 Salvo automaticamente!")
           
#função de listar seus funcionários            
def listar_funcionarios(): #numera eles de acordo com a ordem
    if not funcionarios:
        print("👷‍♂️ Nenhum funcionário cadastrado!")
    else:
        # i = número, f = a ficha do funcionário
        for i, f in enumerate(funcionarios, start=1):
            print(f"{i}º | Nome: {f['nome']} | Idade: {f['idade']} | Cargo: {f['cargo']} | Gênero: {f['genero']}")

#função de pesquisar funcionários
def pesquisar_funcionarios():
    if not funcionarios:
        input("❌️ Nenhum funcionário cadastrado! pressione enter...")
    else:    
        busca = input("💻 Digite o nome do funcionário que gostaria de pesquisar: ").title().strip()
        encontrado = False
        print("----------🔎Resultados da busca🔍----------")
        for i, f in enumerate(funcionarios, start=1):
            if busca in f['nome']:
                print(f"{i}º | Nome: {f['nome']} | Idade: {f['idade']} | Cargo: {f['cargo']} | Gênero: {f['genero']}")
                print("-------------------------------------------")
                encontrado = True
        input("⌨️ pressione enter para continuar...")        
        if not encontrado:
            input("❌️ Nenhum funcionário encontrado! Pressione enter...")

#opcoes das configurações
def ativar_dicas_fn():
    global ativar_dicas
    ativar_dicas = True
    input("✅ Dicas ativadas! Aperte enter...")

def desativar_dicas_fn():
    global ativar_dicas
    ativar_dicas = False
    input("❌ Dicas desativadas! Aperte enter...")

def ativar_salvamento_fn():
    global salvamento_automatico
    salvamento_automatico = True
    input("💾 Salvamento automático ativado! Aperte enter...")

def desativar_salvamento_fn():
    global salvamento_automatico
    salvamento_automatico = False
    input("❌ Salvamento automático desativado! Aperte enter...")

def mostrar_generos_fn():
    global mostrar_generos
    mostrar_generos = True
    input("👥 Gêneros ativados!")

def esconder_generos_fn():
    global mostrar_generos
    mostrar_generos = False
    input("🙇 Gêneros escondidos!")

def mostrar_sugestoes_fn():
    global mostrar_sugestoes
    mostrar_sugestoes = True
    input("💡 Sugestões ativadas!")
    
def esconder_sugestoes_fn():
    global mostrar_sugestoes
    mostrar_sugestoes = False
    input("👷‍♂️ Sugestões escondidas!")
       
acoes_config = {
    "1": ativar_dicas_fn,
    "2": desativar_dicas_fn,
    "3": ativar_salvamento_fn,
    "4": desativar_salvamento_fn,
    "5": mostrar_generos_fn,
    "6": esconder_generos_fn,
    "7": mostrar_sugestoes_fn,
    "8": esconder_sugestoes_fn
}

#Opção das configurações do projeto
def configuracoes():
    while True:
        limpar_tela()
        print("-====+====- ⚙️ Configurações ⚙️ -====+====-")
        print(f"1. Ativar dicas")
        print("2. Desativar dicas")
        print(f"3. Ativar salvamento")
        print("4. Desativar salvamento")
        print(f"5. Mostrar gêneros")
        print("6. Esconder gêneros")
        print("7. Mostrar sugestões")
        print("8. Esconder sugestões")
        print("0. Voltar")
        escolha_conf = input("\n👨‍🏭 O que deseja configurar? ")
        acao = acoes_config.get(escolha_conf)
        if escolha_conf == "0":
            print("↩️ Voltando...")
            time.sleep(1)
            break
        if acao:
            acao()
        else:
            input("❌ Opção inválida! Aperte enter...")

if __name__ == "__main__":
    carregar_dados()
    
    # Agora o loop está devidamente identado dentro do bloco principal
    while escolha != 6:
        menu()
        dicas_layout()
        try:
            escolha = int(input("🚀 Digite o número referente a sua escolha:\n"))
        except:
            input("❌️ Nenhuma opção selecionada! Aperte enter...")
            escolha = 0
            limpar_tela()
            continue # Volta para o início do loop
            
        try:
           if escolha == 1:
              cadastrar_funcionario()
              limpar_tela()
           elif escolha == 2:
              apagar_funcionario()
              limpar_tela()
           elif escolha == 3:
              listar_funcionarios()
              input("pressione enter para continuar...\n")   
              limpar_tela()
           elif escolha == 4:
              pesquisar_funcionarios()
              limpar_tela() 
           elif escolha == 5:
               salvar_dados()
               input("✅️ projeto salvo com sucesso! aperte enter...")   
               limpar_tela()
           elif escolha == 6:
               print("👋 Saindo...")
               break
           elif escolha == 7:
               configuracoes()
               limpar_tela()
           elif escolha > 7 or escolha < 0:
              print("❌️ escolha inválida!")
              time.sleep(1)
              limpar_tela()
              escolha = 0
        except Exception as e:
           input(f"❌️ Erro! aperte enter...")
           limpar_tela()
