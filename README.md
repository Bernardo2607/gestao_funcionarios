<div align="center">

# 💼 Sistema de Gestão de Funcionários

**Um sistema CLI completo para gerenciamento de recursos humanos, com persistência em JSON e interface inteligente no terminal.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/Armazenamento-JSON-F7DF1E?style=for-the-badge&logo=json&logoColor=black)
![Platform](https://img.shields.io/badge/Plataforma-Terminal%20%7C%20CLI-black?style=for-the-badge&logo=gnometerminal&logoColor=white)
![Mobile Dev](https://img.shields.io/badge/Desenvolvido%20em-Pydroid%203%20📱-4CAF50?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

</div>

---

## 📌 Visão Geral

O **Sistema de Gestão de Funcionários** é uma aplicação de terminal (CLI) desenvolvida em Python puro, que oferece um fluxo completo de CRUD para gerenciamento de pessoas em uma organização. Os dados são persistidos localmente em formato JSON, garantindo que nenhuma informação seja perdida entre sessões.

O projeto foi construído com foco em organização de código, experiência de uso no terminal e boas práticas de lógica de programação — tudo isso desenvolvido **inteiramente em um dispositivo mobile**, utilizando o aplicativo **Pydroid 3**.

> 🎯 Objetivo principal: demonstrar domínio de lógica orientada a objetos, persistência de dados e estruturação de sistemas em Python, independentemente do ambiente de desenvolvimento.

---

## ✨ Funcionalidades

### 👤 Gestão de Funcionários (CRUD)
- **Cadastrar** — Registra nome, idade, cargo e gênero de cada funcionário
- **Listar** — Exibe todos os funcionários cadastrados de forma numerada e organizada
- **Pesquisar** — Localiza funcionários por nome com sistema de busca dinâmica
- **Remover** — Deleta registros individualmente ou limpa todos de uma vez, com confirmação

### 💾 Persistência de Dados
- Salvamento **manual** sob demanda
- Salvamento **automático** após cada operação (ativável nas configurações)
- Dados armazenados em `funcionarios.json` com encoding UTF-8

### 📊 Relatório Automático
- Gera um arquivo `relatorio.csv` com planilha completa dos dados
- Inclui timestamp, total de funcionários e estatísticas por gênero

### ⚙️ Sistema de Configurações
| Opção | Descrição |
|---|---|
| Dicas aleatórias | Exibe insights sobre gestão de pessoas e diversidade |
| Salvamento automático | Persiste dados após cada ação automaticamente |
| Estatísticas de gênero | Mostra contagem de Masculino / Feminino / Outro no menu |
| Sugestão de cargos | Sugere cargos já cadastrados ao registrar novos funcionários |

### 🧠 Interface Inteligente
- Menu principal com contador de funcionários em tempo real
- Sistema de **dicas aleatórias** sobre gestão e diversidade organizacional
- Feedback visual com emojis para cada ação do sistema
- Tratamento de erros em todas as entradas do usuário

---

## 🏗️ Estrutura do Sistema

```
📁 gestao-funcionarios/
├── 📄 main.py               # Arquivo principal — lógica e fluxo do sistema
├── 📄 funcionarios.json     # Banco de dados local (gerado automaticamente)
└── 📄 relatorio.txt         # Relatório exportável (gerado sob demanda)
```

### Arquitetura Interna

```
main.py
├── class Funcionario          → Modelo de dados com serialização para dict
├── salvar_dados()             → Persistência: lista → JSON
├── carregar_dados()           → Hidratação: JSON → objetos Funcionario
├── menu()                     → Interface principal com estatísticas dinâmicas
├── cadastrar_funcionario()    → CREATE com validação de gênero e sugestão de cargo
├── apagar_funcionario()       → DELETE individual ou em massa com confirmação
├── listar_funcionarios()      → READ com enumeração indexada
├── pesquisar_funcionarios()   → READ filtrado por substring do nome
├── gerar_relatorio()          → Export para .csv
├── configuracoes()            → Submenu com 8 opções de personalização
└── acoes_menu {}              → Dicionário de dispatch para o loop principal
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso no Projeto |
|---|---|
| `Python 3` | Linguagem principal — lógica, OOP e fluxo de dados |
| `json` | Serialização e leitura da base de dados local |
| `os` | Limpeza de tela e verificação de existência de arquivos |
| `csv` | Utilizado na geração de planilhas |
| `random` | Seleção aleatória de dicas no menu |
| `time` | Pausas de feedback visual entre ações |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado ([download aqui](https://www.python.org/downloads/))
- Nenhuma dependência externa — apenas bibliotecas nativas do Python

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gestao-funcionarios.git

# 2. Acesse a pasta do projeto
cd gestao-funcionarios

# 3. Execute o sistema
python main.py
```

> 📱 **No celular com Pydroid 3?** Basta abrir o arquivo `main.py` e tocar em **Run**.

---

## 📱 Desenvolvido 100% no Celular

Este projeto tem um diferencial que vale ser destacado: **foi escrito completamente em um dispositivo mobile**, utilizando o app **[Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)** para Android.

Isso demonstra que o aprendizado de programação não depende de um setup caro ou de um computador. Com foco e organização, é possível estruturar sistemas completos com OOP, persistência de dados e tratamento de erros — direto do celular.

---

## 🎯 Objetivos do Projeto

Este sistema foi desenvolvido com os seguintes objetivos de aprendizado e portfólio:

- ✅ Praticar **Programação Orientada a Objetos** com Python
- ✅ Implementar **persistência de dados** sem banco de dados externo
- ✅ Estruturar um projeto com **separação de responsabilidades** clara
- ✅ Desenvolver **tratamento de erros** robusto em aplicações CLI
- ✅ Criar uma **experiência de usuário** agradável no terminal
- ✅ Provar que é possível programar com qualidade em qualquer ambiente

---

## 💡 Diferenciais Técnicos

- **Dispatch por dicionário** — O loop principal usa `dict` de funções em vez de `if/elif` encadeados, tornando o código mais limpo e extensível
- **Serialização bidirecional** — A classe `Funcionario` converte nativamente para `dict` (via `para_dict()`) e é reconstruída a partir do JSON via `**kwargs`
- **Configurações em runtime** — Todas as flags de comportamento são alteradas em tempo de execução via `globals()`, sem reinicialização
- **Zero dependências externas** — O projeto roda em qualquer ambiente Python 3 sem instalação de pacotes

---

## 👨‍💻 Autor

**Bernardo**
Desenvolvedor focado em lógica de programação, backend e segurança de dados.

[![GitHub](https://img.shields.io/badge/GitHub-Bernardo2607-181717?style=flat-square&logo=github)](https://github.com/seu-usuario)

---

<div align="center">

*Feito com 💻 + 📱 e muito Python*

</div>
