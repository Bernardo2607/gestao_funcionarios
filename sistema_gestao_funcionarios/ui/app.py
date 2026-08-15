import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.funcionarios import FuncionariosView
from ui.cadastro import CadastroFuncionario
from ui.relatorios import RelatoriosView
from ui.configuracoes import ConfiguracoesView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Funcionários")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self, self.mudar_tela)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.telas = {}
        self.tela_atual = None

        self.criar_telas()
        self.mudar_tela("dashboard")

    def criar_telas(self):
        self.telas["dashboard"] = Dashboard(self.main_frame, self)
        self.telas["funcionarios"] = FuncionariosView(self.main_frame, self)
        self.telas["relatorios"] = RelatoriosView(self.main_frame, self)
        self.telas["configuracoes"] = ConfiguracoesView(self.main_frame, self)

    def mudar_tela(self, nome_tela):
        if self.tela_atual:
            self.tela_atual.grid_forget()

        self.tela_atual = self.telas[nome_tela]
        self.tela_atual.grid(row=0, column=0, sticky="nswe")
        self.sidebar.atualizar_selecao(nome_tela)

    def abrir_cadastro(self, modo="novo", dados=None):
        """Abre o formulário de cadastro/edição.

        Garante que não existam janelas duplicadas abertas — fecha a pré-existente antes de abrir uma nova.
        """
        # Se já houver uma janela de cadastro aberta, fecha-a para evitar duplicação
        try:
            existing = getattr(self, "_cadastro_win", None)
            if existing and existing.winfo_exists():
                try:
                    existing.destroy()
                except Exception:
                    pass
        except Exception:
            pass

        win = CadastroFuncionario(self, modo=modo, dados=dados)
        # guarda referência para evitar múltiplas janelas e limpar referência quando for destruída
        self._cadastro_win = win
        try:
            win.bind("<Destroy>", lambda e: setattr(self, "_cadastro_win", None))
        except Exception:
            # alguns backends podem não suportar bind em Toplevel — ignore
            pass
        return win

    def mostrar_aviso(self, mensagem, title="Aviso", auto_close=3000):
        """Mostra uma mensagem breve ao usuário.

        Se auto_close for None, mostra um modal com botão OK. Caso contrário, fecha automaticamente após auto_close ms.
        """
        dlg = ctk.CTkToplevel(self)
        dlg.title(title)
        dlg.geometry('420x120')
        try:
            if auto_close is None:
                dlg.transient(self)
                dlg.grab_set()
            ctk.CTkLabel(dlg, text=mensagem, font=ctk.CTkFont(size=13), wraplength=380).pack(pady=(20,10))
            if auto_close is None:
                ctk.CTkButton(dlg, text='OK', width=100, command=dlg.destroy).pack()
            else:
                # fecha automaticamente
                dlg.after(auto_close, dlg.destroy)
        except Exception:
            # fallback: destroy if something fails
            dlg.after(1500, dlg.destroy)
