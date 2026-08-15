import customtkinter as ctk
from Database.database import inserir_funcionario, atualizar_funcionario

# Design tokens
FONT_FAMILY = "Inter"
SURFACE = "#0f1724"
TEXT = "#E6EEF8"
ACCENT = "#4F46E5"

class CadastroFuncionario(ctk.CTkToplevel):
    def __init__(self, parent, modo="novo", dados=None):
        super().__init__(parent)
        self.modo = modo
        self.dados = dados or {}

        titulo = "Cadastrar Funcionário" if modo == "novo" else "Editar Funcionário"
        self.title(titulo)
        self.geometry("520x620")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (520 // 2)
        y = (self.winfo_screenheight() // 2) - (620 // 2)
        self.geometry(f"+{x}+{y}")

        self.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=30, pady=(25, 20))

        icone = "➕" if modo == "novo" else "✏️"
        self.titulo = ctk.CTkLabel(
            self.header,
            text=f"{icone} {titulo}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self.header,
            text="Preencha os dados do funcionário abaixo.",
            font=ctk.CTkFont(size=12),
            text_color="#888899"
        )
        self.subtitulo.pack(anchor="w", pady=(4, 0))

        # Formulário
        self.form_frame = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        self.form_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))
        self.form_frame.grid_columnconfigure(0, weight=1)

        campos = [
            ("nome", "Nome completo", "entry"),
            ("genero", "Gênero", "option", ["Masculino", "Feminino", "Outro", "Prefiro não informar"]),
            ("cargo", "Cargo", "entry"),
            ("email", "E-mail", "entry"),
            ("salario", "Salário", "entry"),
        ]

        self.widgets = {}
        for idx, (chave, label, tipo, *extra) in enumerate(campos):
            lbl = ctk.CTkLabel(
                self.form_frame,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#a0a0b0"
            )
            lbl.grid(row=idx*2, column=0, padx=20, pady=(18 if idx == 0 else 12, 6), sticky="w")

            if tipo == "entry":
                widget = ctk.CTkEntry(
                    self.form_frame,
                    height=40,
                    corner_radius=10,
                    font=ctk.CTkFont(size=13)
                )
            elif tipo == "option":
                widget = ctk.CTkOptionMenu(
                    self.form_frame,
                    values=extra[0],
                    height=40,
                    corner_radius=10,
                    font=ctk.CTkFont(size=13),
                    dropdown_font=ctk.CTkFont(size=12)
                )

            widget.grid(row=idx*2+1, column=0, padx=20, pady=(0, 0), sticky="ew")
            self.widgets[chave] = widget

        # Preencher dados no modo edição (robusto: cada campo em try/except para evitar janela vazia por erro)
        if modo == "editar" and dados:
            try:
                self.widgets["nome"].insert(0, str(dados.get("nome", "")))
            except Exception:
                pass
            # genero pode ser um OptionMenu; tente setar com fallback silencioso
            try:
                genero_widget = self.widgets.get("genero")
                genero_val = dados.get("genero", "")
                if hasattr(genero_widget, 'set'):
                    try:
                        genero_widget.set(genero_val or "")
                    except Exception:
                        # se valor não estiver nas opções, tente configurar temporariamente
                        try:
                            existing = list(genero_widget._options) if hasattr(genero_widget, '_options') else None
                        except Exception:
                            existing = None
                        try:
                            genero_widget.set("")
                        except Exception:
                            pass
                else:
                    # se não for optionmenu, trate como entry
                    genero_widget.delete(0, 'end')
                    genero_widget.insert(0, genero_val)
            except Exception:
                pass

            try:
                self.widgets["cargo"].delete(0, 'end')
                self.widgets["cargo"].insert(0, str(dados.get("cargo", "")))
            except Exception:
                pass
            try:
                self.widgets["email"].delete(0, 'end')
                self.widgets["email"].insert(0, str(dados.get("email", "")))
            except Exception:
                pass
            try:
                # garantir string com ponto decimal
                sal = dados.get("salario", "")
                self.widgets["salario"].delete(0, 'end')
                self.widgets["salario"].insert(0, str(sal))
            except Exception:
                pass

        # Botões
        self.botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.botoes_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(10, 25))
        self.botoes_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_cancelar = ctk.CTkButton(
            self.botoes_frame,
            text="Cancelar",
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#555566",
            hover_color="#444455",
            command=self.destroy
        )
        self.btn_cancelar.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        cor_salvar = "#3b82f6" if modo == "novo" else "#f59e0b"
        hover_salvar = "#2563eb" if modo == "novo" else "#d97706"
        texto_salvar = "Salvar cadastro" if modo == "novo" else "Salvar alterações"

        self.btn_salvar = ctk.CTkButton(
            self.botoes_frame,
            text=texto_salvar,
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=cor_salvar,
            hover_color=hover_salvar,
            command=self.salvar_demo
        )
        self.btn_salvar.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def salvar_demo(self):
        """Valida e persiste os dados no banco (inserir ou atualizar)."""
        # Coleta valores do formulário
        nome = self.widgets["nome"].get().strip()
        genero = self.widgets["genero"].get() if hasattr(self.widgets["genero"], "get") else self.widgets["genero"].get()
        cargo = self.widgets["cargo"].get().strip()
        email = self.widgets["email"].get().strip()
        salario_raw = self.widgets["salario"].get().strip()

        if not nome:
            self.mostrar_erro("Nome é obrigatório.")
            return

        # Normalizar salário: aceita formatos 1.234,56 e 1234.56
        def parse_salary(s: str) -> float:
            s = s.replace("R$", "").replace(" ", "").strip()
            if s == "":
                return 0.0
            # brasil: '1.234,56' -> remove '.' thousands, convert ',' to '.'
            if "," in s and "." in s and s.rfind(",") > s.rfind("."):
                s = s.replace('.', '').replace(',', '.')
            elif "," in s and "." not in s:
                s = s.replace(',', '.')
            # else assume dot-decimal or plain number
            return float(s)

        try:
            salario = parse_salary(salario_raw)
        except Exception:
            self.mostrar_erro("Salário em formato inválido.")
            return

        dados = {
            "nome": nome,
            "genero": genero,
            "cargo": cargo,
            "email": email,
            "salario": salario,
        }

        try:
            if self.modo == "novo":
                new_id = inserir_funcionario(dados)
            else:
                # precisa do id para atualizar
                if not self.dados or not self.dados.get("id"):
                    self.mostrar_erro("ID do funcionário ausente para atualização.")
                    return
                dados["id"] = int(self.dados["id"])
                atualizar_funcionario(dados)
        except Exception as e:
            self.mostrar_erro(f"Falha ao salvar: {e}")
            return

        # Atualiza a listagem e o dashboard na tela principal, se disponíveis
        try:
            if hasattr(self.master, "telas"):
                if "funcionarios" in self.master.telas:
                    self.master.telas["funcionarios"].carregar_dados()
                if "dashboard" in self.master.telas and hasattr(self.master.telas["dashboard"], "update_stats"):
                    # atualiza os cards do dashboard imediatamente
                    try:
                        self.master.telas["dashboard"].update_stats()
                    except Exception:
                        pass
        except Exception:
            pass

        # Confirmação e fechamento
        dialog = ctk.CTkToplevel(self)
        dialog.title("Informação")
        dialog.geometry("350x140")
        dialog.transient(self)
        dialog.grab_set()

        acao = "cadastrado" if self.modo == "novo" else "atualizado"
        ctk.CTkLabel(dialog, text=f"Funcionário {acao} com sucesso.", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
        ctk.CTkButton(dialog, text="OK", width=100, command=lambda: [dialog.destroy(), self.destroy()]).pack()

    def mostrar_erro(self, mensagem):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Erro")
        dialog.geometry("360x140")
        dialog.transient(self)
        dialog.grab_set()
        ctk.CTkLabel(dialog, text=mensagem, font=ctk.CTkFont(size=13), wraplength=320, text_color="#ff6b6b").pack(pady=(25, 15))
        ctk.CTkButton(dialog, text="OK", width=100, command=dialog.destroy).pack()
