import customtkinter as ctk

# Design tokens
FONT_FAMILY = "Inter"
BG = "#0b1220"
SURFACE = "#0f1724"
MUTED = "#94A3B8"
TEXT = "#E6EEF8"
ACCENT = "#4F46E5"
ACCENT_HOVER = "#4338CA"

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, mudar_tela_callback):
        super().__init__(parent, width=240, corner_radius=0, fg_color=SURFACE)
        self.mudar_tela = mudar_tela_callback
        self.grid_rowconfigure(5, weight=1)

        self.botoes = {}
        self.botao_selecionado = None

        # Logo / Título
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(24, 28), sticky="w")

        self.icone_logo = ctk.CTkLabel(self.logo_frame, text="👥", font=ctk.CTkFont(family=FONT_FAMILY, size=26))
        self.icone_logo.pack(side="left", padx=(0, 10))

        self.titulo_logo = ctk.CTkLabel(
            self.logo_frame,
            text="Gestão de Funcionários",
            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
            text_color=TEXT
        )
        self.titulo_logo.pack(side="left")

        # Separador
        self.separador = ctk.CTkFrame(self, height=1, fg_color="#142035")
        self.separador.grid(row=1, column=0, sticky="ew", padx=15, pady=(8, 18))

        # Itens do menu
        itens = [
            ("dashboard", "🏠", "Início"),
            ("funcionarios", "👥", "Funcionários"),
            ("relatorios", "📊", "Relatórios"),
            ("configuracoes", "⚙️", "Configurações"),
        ]

        for idx, (chave, icone, texto) in enumerate(itens, start=2):
            btn = ctk.CTkButton(
                self,
                text=f"  {icone}  {texto}",
                anchor="w",
                height=44,
                corner_radius=12,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                fg_color="transparent",
                hover_color="#152039",
                text_color=MUTED,
                command=lambda c=chave: self.mudar_tela(c)
            )
            btn.grid(row=idx, column=0, padx=14, pady=6, sticky="ew")
            self.botoes[chave] = btn

        # Versão no rodapé
        self.versao = ctk.CTkLabel(
            self,
            text="v1.0.0",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=MUTED
        )
        self.versao.grid(row=6, column=0, pady=14)

    def atualizar_selecao(self, chave_ativa):
        for chave, btn in self.botoes.items():
            if chave == chave_ativa:
                btn.configure(
                    fg_color=ACCENT,
                    text_color=TEXT,
                    font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=MUTED,
                    font=ctk.CTkFont(family=FONT_FAMILY, size=13)
                )
