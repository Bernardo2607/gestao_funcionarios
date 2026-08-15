import customtkinter as ctk
from Database.database import contar_funcionarios, contar_cargos, media_salarial, pesquisar_funcionarios, backup_db

# Design tokens
FONT_FAMILY = "Inter"
SURFACE = "#0f1724"
TEXT = "#E6EEF8"
ACCENT = "#4F46E5"

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 25))

        self.titulo = ctk.CTkLabel(
            self.header,
            text="Bem-vindo ao Sistema",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self.header,
            text="Aqui está um resumo da sua equipe",
            font=ctk.CTkFont(size=14),
            text_color="#888899"
        )
        self.subtitulo.pack(anchor="w", pady=(4, 0))

        # Cards de estatísticas (valores reais do banco)
        try:
            num_func = contar_funcionarios()
            num_cargos = contar_cargos()
            media = media_salarial()
        except Exception:
            num_func = 0
            num_cargos = 0
            media = 0.0

        # criar cards e manter referência aos labels de valor para atualização posterior
        card, self.valor_func_lbl = self.criar_card("👥", str(num_func), "Funcionários", ACCENT)
        card.grid(row=1, column=0, padx=(0, 12), pady=(0, 20), sticky="nsew")

        card, self.valor_cargos_lbl = self.criar_card("💼", str(num_cargos), "Cargos", ACCENT)
        card.grid(row=1, column=1, padx=(6, 6), pady=(0, 20), sticky="nsew")

        card, self.valor_media_lbl = self.criar_card("💰", f"R$ {media:,.2f}", "Média Salarial", ACCENT)
        card.grid(row=1, column=2, padx=(12, 0), pady=(0, 20), sticky="nsew")

        # Área de pesquisa rápida
        self.pesquisa_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=SURFACE)
        self.pesquisa_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        self.pesquisa_frame.grid_columnconfigure(0, weight=1)

        self.pesquisa_label = ctk.CTkLabel(
            self.pesquisa_frame,
            text="🔎 Pesquisar funcionário",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.pesquisa_label.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="w")

        self.pesquisa_input_frame = ctk.CTkFrame(self.pesquisa_frame, fg_color="transparent")
        self.pesquisa_input_frame.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="ew")
        self.pesquisa_input_frame.grid_columnconfigure(0, weight=1)

        self.pesquisa_entry = ctk.CTkEntry(
            self.pesquisa_input_frame,
            placeholder_text="Digite nome, cargo ou e-mail...",
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13)
        )
        self.pesquisa_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.pesquisa_btn = ctk.CTkButton(
            self.pesquisa_input_frame,
            text="Pesquisar",
            width=120,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.pesquisar_demo
        )
        self.pesquisa_btn.grid(row=0, column=1)

        # Ações rápidas
        self.acoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.acoes_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

        self.acoes_label = ctk.CTkLabel(
            self.acoes_frame,
            text="⚡ Ações rápidas",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.acoes_label.pack(anchor="w", pady=(0, 12))

        self.btn_cadastrar = ctk.CTkButton(
            self.acoes_frame,
            text="+  Cadastrar funcionário",
            width=220,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=lambda: self.controller.abrir_cadastro()
        )
        self.btn_cadastrar.pack(anchor="w", pady=(0, 10))

        self.btn_listar = ctk.CTkButton(
            self.acoes_frame,
            text="🔎  Pesquisar funcionários",
            width=220,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=lambda: self.controller.mudar_tela("funcionarios")
        )
        self.btn_listar.pack(anchor="w")

        # Botão de backup (removido backup automático no startup; botão na dashboard)
        self.btn_backup = ctk.CTkButton(
            self.acoes_frame,
            text="🗄️  Gerar backup",
            width=220,
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self._do_backup
        )
        self.btn_backup.pack(anchor="w", pady=(10,0))

    def criar_card(self, icone, valor, descricao, cor):
        """Cria um card e retorna (card, label_valor) para permitir atualizações posteriores."""
        card = ctk.CTkFrame(self, corner_radius=16, fg_color="#1e1e2e", height=130)
        card.grid_propagate(False)

        icone_lbl = ctk.CTkLabel(
            card,
            text=icone,
            font=ctk.CTkFont(size=32)
        )
        icone_lbl.pack(anchor="w", padx=20, pady=(18, 0))

        valor_lbl = ctk.CTkLabel(
            card,
            text=valor,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=cor
        )
        valor_lbl.pack(anchor="w", padx=20, pady=(6, 0))

        desc_lbl = ctk.CTkLabel(
            card,
            text=descricao,
            font=ctk.CTkFont(size=13),
            text_color="#888899"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(2, 18))

        return card, valor_lbl

    def update_stats(self):
        """Recalcula e atualiza os valores exibidos nos cards.

        Chamado depois de operações que alteram os dados (ex.: inserir/atualizar/excluir).
        """
        try:
            num_func = contar_funcionarios()
            num_cargos = contar_cargos()
            media = media_salarial()
        except Exception:
            num_func = 0
            num_cargos = 0
            media = 0.0

        try:
            self.valor_func_lbl.configure(text=str(num_func))
        except Exception:
            pass
        try:
            self.valor_cargos_lbl.configure(text=str(num_cargos))
        except Exception:
            pass
        try:
            self.valor_media_lbl.configure(text=f"R$ {media:,.2f}")
        except Exception:
            pass

    def _do_backup(self):
        """Trigger a safe backup and notify the user with a short, non-blocking message."""
        try:
            out = backup_db()
            # use controller's helper to show a brief message (auto-close)
            try:
                self.controller.mostrar_aviso(f"Backup criado: {out}", title="Backup concluído", auto_close=3500)
            except Exception:
                # fallback: simple dialog
                dlg = ctk.CTkToplevel(self)
                dlg.title("Backup concluído")
                dlg.geometry('420x120')
                ctk.CTkLabel(dlg, text=f"Backup criado: {out}", wraplength=380).pack(pady=(20,10))
                ctk.CTkButton(dlg, text='OK', width=100, command=dlg.destroy).pack()
        except Exception as e:
            try:
                self.controller.mostrar_aviso(f"Falha ao criar backup: {e}", title="Erro", auto_close=3500)
            except Exception:
                dlg = ctk.CTkToplevel(self)
                dlg.title("Erro")
                dlg.geometry('420x120')
                ctk.CTkLabel(dlg, text=f"Falha ao criar backup: {e}", wraplength=380).pack(pady=(20,10))
                ctk.CTkButton(dlg, text='OK', width=100, command=dlg.destroy).pack()

    def pesquisar_demo(self):
        termo = self.pesquisa_entry.get().strip()
        if not termo:
            self.mostrar_aviso("Digite um termo para pesquisar.")
            return

        try:
            resultados = pesquisar_funcionarios(termo)
            total = len(resultados)
        except Exception:
            resultados = []
            total = 0

        # Abre diálogo com resumo e opção de abrir a listagem já com o filtro aplicado
        dialog = ctk.CTkToplevel(self)
        dialog.title("Pesquisa")
        dialog.geometry("420x180")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=f'Pesquisa por "{termo}"', font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(12, 6))
        ctk.CTkLabel(dialog, text=f"{total} resultado(s) encontrados.", font=ctk.CTkFont(size=12), wraplength=380).pack(pady=(0, 12))

        def abrir_listagem_filtrada():
            dialog.destroy()
            # mudar para a tela de funcionarios e aplicar o filtro
            self.controller.mudar_tela("funcionarios")
            try:
                view = self.controller.telas["funcionarios"]
                # preenche o campo de busca e executa o filtro na própria view
                view.filtro_entry.delete(0, 'end')
                view.filtro_entry.insert(0, termo)
                # garante que cargo volta ao default
                try:
                    view.filtro_cargo.set("Todos os cargos")
                except Exception:
                    pass
                view.filtrar_demo()
            except Exception:
                pass

        ctk.CTkButton(dialog, text="Abrir listagem", width=160, command=abrir_listagem_filtrada).pack(pady=(6, 6))
        ctk.CTkButton(dialog, text="OK", width=100, command=dialog.destroy).pack()
