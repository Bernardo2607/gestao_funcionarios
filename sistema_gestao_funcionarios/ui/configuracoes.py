import customtkinter as ctk

class ConfiguracoesView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        self.titulo = ctk.CTkLabel(
            self.header,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self.header,
            text="Personalize a aparência e o comportamento do sistema",
            font=ctk.CTkFont(size=13),
            text_color="#888899"
        )
        self.subtitulo.pack(anchor="w", pady=(4, 0))

        # Seção Aparência
        self.aparencia_frame = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        self.aparencia_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.aparencia_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.aparencia_frame,
            text="🎨 Aparência",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(18, 12), sticky="w")

        self.tema_frame = ctk.CTkFrame(self.aparencia_frame, fg_color="transparent")
        self.tema_frame.grid(row=1, column=0, padx=20, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(self.tema_frame, text="Tema", font=ctk.CTkFont(size=13, weight="bold"), text_color="#a0a0b0").pack(anchor="w")

        # default selected label for segmented button matches available values
        self.tema_var = ctk.StringVar(value="Escuro")
        self.tema_segment = ctk.CTkSegmentedButton(
            self.tema_frame,
            values=["Claro", "Escuro", "Sistema"],
            variable=self.tema_var,
            height=36,
            font=ctk.CTkFont(size=13),
            command=self.mudar_tema
        )
        self.tema_segment.pack(fill="x", pady=(8, 0))


        # Seção Preferências
        self.pref_frame = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        self.pref_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        # Preferências: usar cor de texto adaptativa para permanecer legível em todos os temas
        try:
            mode = ctk.get_appearance_mode()
        except Exception:
            mode = 'dark'
        pref_color = '#E6EEF8' if mode == 'dark' else '#111827'
        self.pref_title = ctk.CTkLabel(
            self.pref_frame,
            text="🔔 Preferências",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=pref_color
        )
        self.pref_title.grid(row=0, column=0, padx=20, pady=(18, 12), sticky="w")

        opcoes = [
            ("Exibir notificações de aniversariantes", True),
            ("Confirmar antes de excluir registros", True),
            ("Abrir na tela de funcionários ao iniciar", False),
        ]

        self.checks = []
        for idx, (texto, padrao) in enumerate(opcoes, start=1):
            var = ctk.BooleanVar(value=padrao)
            chk = ctk.CTkCheckBox(
                self.pref_frame,
                text=texto,
                variable=var,
                font=ctk.CTkFont(size=13),
                corner_radius=6,
                border_width=2
            )
            chk.grid(row=idx, column=0, padx=20, pady=(0, 12 if idx == len(opcoes) else 8), sticky="w")
            self.checks.append((var, chk))

        # Seção Sobre
        self.sobre_frame = ctk.CTkFrame(self, corner_radius=14, fg_color="#1e1e2e")
        self.sobre_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(
            self.sobre_frame,
            text="ℹ️ Sobre",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(18, 8), sticky="w")

        ctk.CTkLabel(
            self.sobre_frame,
            text="Sistema de Gestão de Funcionários v1.0.0\nDesenvolvido com Python + CustomTkinter",
            font=ctk.CTkFont(size=12),
            text_color="#888899",
            justify="left"
        ).grid(row=1, column=0, padx=20, pady=(0, 18), sticky="w")

    def mudar_tema(self, valor):
        modo = {"Claro": "light", "Escuro": "dark", "Sistema": "system"}
        ctk.set_appearance_mode(modo.get(valor, "dark"))
        # atualizar cores adaptativas dos títulos para manter legibilidade
        try:
            mode = ctk.get_appearance_mode()
        except Exception:
            mode = 'dark'
        new_color = '#E6EEF8' if mode == 'dark' else '#111827'
        try:
            if hasattr(self, 'pref_title') and self.pref_title is not None:
                self.pref_title.configure(text_color=new_color)
        except Exception:
            pass
