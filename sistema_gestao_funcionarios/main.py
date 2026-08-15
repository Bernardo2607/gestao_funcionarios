import customtkinter as ctk
from ui.app import App
from Database.database import inicializar_banco
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    inicializar_banco()
    app = App()
    app.mainloop()
