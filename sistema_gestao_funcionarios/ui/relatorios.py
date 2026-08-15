import customtkinter as ctk
from Database.database import listar_funcionarios, _get_connection
import csv
import os
from datetime import datetime

# Design tokens
FONT_FAMILY = "Inter"
SURFACE = "#0f1724"
TEXT = "#E6EEF8"
MUTED = "#94A3B8"
ACCENT = "#4F46E5"

class RelatoriosView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Cabeçalho
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        # Let CTk adapt label colors automatically to the current theme (avoid hard-coded light text)
        self.titulo = ctk.CTkLabel(
            self.header,
            text="📊 Relatórios",
            font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold")
        )
        self.titulo.pack(anchor="w")

        self.subtitulo = ctk.CTkLabel(
            self.header,
            text="Gere relatórios personalizados sobre sua equipe",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.subtitulo.pack(anchor="w", pady=(4, 0))

        # Painel de filtros
        self.filtros_frame = ctk.CTkFrame(self, corner_radius=14, fg_color=SURFACE)
        self.filtros_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.filtros_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Tipo de relatório
        self.tipo_frame = ctk.CTkFrame(self.filtros_frame, fg_color="transparent")
        self.tipo_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        ctk.CTkLabel(self.tipo_frame, text="Tipo de relatório", font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"), text_color=MUTED).pack(anchor="w")
        self.tipo_combo = ctk.CTkOptionMenu(
            self.tipo_frame,
            values=["Relatório geral de funcionários", "Folha de pagamento", "Análise de cargos", "Turnover"],
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13)
        )
        self.tipo_combo.pack(fill="x", pady=(6, 0))

        # Período início
        self.periodo_inicio_frame = ctk.CTkFrame(self.filtros_frame, fg_color="transparent")
        self.periodo_inicio_frame.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        ctk.CTkLabel(self.periodo_inicio_frame, text="Data início", font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"), text_color=MUTED).pack(anchor="w")
        self.data_inicio = ctk.CTkEntry(self.periodo_inicio_frame, placeholder_text="DD/MM/AAAA", height=38, corner_radius=10, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
        self.data_inicio.pack(fill="x", pady=(6, 0))

        # Período fim
        self.periodo_fim_frame = ctk.CTkFrame(self.filtros_frame, fg_color="transparent")
        self.periodo_fim_frame.grid(row=0, column=2, padx=15, pady=15, sticky="ew")

        ctk.CTkLabel(self.periodo_fim_frame, text="Data fim", font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"), text_color=MUTED).pack(anchor="w")
        self.data_fim = ctk.CTkEntry(self.periodo_fim_frame, placeholder_text="DD/MM/AAAA", height=38, corner_radius=10, font=ctk.CTkFont(family=FONT_FAMILY, size=13))
        self.data_fim.pack(fill="x", pady=(6, 0))

        # bind focus-out for formatting
        try:
            self.data_inicio.bind("<FocusOut>", lambda e: self._format_entry(self.data_inicio))
            self.data_fim.bind("<FocusOut>", lambda e: self._format_entry(self.data_fim))
        except Exception:
            pass

        # Área de visualização
        self.visualizacao_frame = ctk.CTkFrame(self, corner_radius=14, fg_color=SURFACE)
        self.visualizacao_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        self.visualizacao_frame.grid_columnconfigure(0, weight=1)
        self.visualizacao_frame.grid_rowconfigure(1, weight=1)

        self.vis_header = ctk.CTkLabel(
            self.visualizacao_frame,
            text="📄 Pré-visualização do relatório",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=MUTED
        )
        self.vis_header.grid(row=0, column=0, padx=20, pady=(18, 10), sticky="w")

        self.vis_area = ctk.CTkTextbox(
            self.visualizacao_frame,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            fg_color="#081020",
            text_color=TEXT,
            state="normal"
        )
        self.vis_area.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="nsew")
        self.vis_area.insert("0.0", "Selecione os filtros e clique em \"Gerar relatório\" para visualizar.\n\nEste espaço será preenchido com os dados do relatório quando o sistema estiver integrado ao banco de dados.")
        self.vis_area.configure(state="disabled")

        # Botões
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, sticky="ew", pady=(0,12))

        self.btn_gerar = ctk.CTkButton(
            self.buttons_frame,
            text="📊 Gerar relatório",
            height=46,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color="#3b32b6",
            command=self.gerar_relatorio
        )
        self.btn_gerar.pack(side="left", padx=(20,8))

        self.btn_export = ctk.CTkButton(
            self.buttons_frame,
            text="⬇️ Exportar CSV",
            height=46,
            corner_radius=12,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color="#0f1724",
            hover_color="#111827",
            command=self.export_csv
        )
        self.btn_export.pack(side="left")

        self.current_report = None

    def _format_entry(self, entry):
        """Format and validate date entry (on focus out) into DD/MM/YYYY if possible.

        This function attempts several common normalizations silently and will clear the
        field when it cannot be parsed — no modal dialogs are shown.
        """
        txt = entry.get().strip()
        if not txt:
            return
        # quick normalize common separators
        s = txt.replace('.', '/').replace('-', '/').replace(' ', '')
        # try direct parse
        try:
            parsed = self._parse_date(s)
            entry.delete(0, 'end')
            entry.insert(0, parsed.strftime('%d/%m/%Y'))
            return
        except Exception:
            pass
        # try heuristic for 8-digit numbers (YYYYMMDD or DDMMYYYY)
        digits = ''.join([c for c in s if c.isdigit()])
        if len(digits) == 8:
            # guess YYYYMMDD if first 4 digits look like a year
            try:
                if int(digits[:4]) >= 1900:
                    parsed = datetime.strptime(digits, '%Y%m%d')
                    entry.delete(0, 'end')
                    entry.insert(0, parsed.strftime('%d/%m/%Y'))
                    return
                else:
                    parsed = datetime.strptime(digits, '%d%m%Y')
                    entry.delete(0, 'end')
                    entry.insert(0, parsed.strftime('%d/%m/%Y'))
                    return
            except Exception:
                pass
        # if all attempts fail, clear the entry silently (no pop-up) so downstream logic isn't blocked
        entry.delete(0, 'end')
        return

    def _parse_date(self, s: str) -> datetime:
        """Try multiple common date formats and return a datetime.date object.

        Raises ValueError if no format matches.
        """
        s = s.strip()
        fmts = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y', '%Y/%m/%d']
        for f in fmts:
            try:
                return datetime.strptime(s, f)
            except Exception:
                continue
        # Try to parse ISO formats
        try:
            return datetime.fromisoformat(s)
        except Exception:
            pass
        raise ValueError('Formato de data desconhecido')

    def _show_message(self, title, message):
        dlg = ctk.CTkToplevel(self)
        dlg.title(title)
        dlg.geometry('360x140')
        dlg.transient(self.winfo_toplevel())
        dlg.grab_set()
        ctk.CTkLabel(dlg, text=message, font=ctk.CTkFont(size=13), wraplength=320).pack(pady=(24, 12))
        ctk.CTkButton(dlg, text='OK', width=100, command=dlg.destroy).pack()

    def gerar_relatorio(self):
        tipo = self.tipo_combo.get()
        # Validate and reformat dates
        inicio = self.data_inicio.get().strip()
        fim = self.data_fim.get().strip()
        data_inicio_dt = None
        data_fim_dt = None
        if inicio:
            try:
                data_inicio_dt = self._parse_date(inicio)
                self.data_inicio.delete(0, 'end')
                self.data_inicio.insert(0, data_inicio_dt.strftime('%d/%m/%Y'))
            except ValueError:
                # silently clear invalid date (no modal) — report generation will proceed without a start date
                self.data_inicio.delete(0, 'end')
                data_inicio_dt = None
        if fim:
            try:
                data_fim_dt = self._parse_date(fim)
                self.data_fim.delete(0, 'end')
                self.data_fim.insert(0, data_fim_dt.strftime('%d/%m/%Y'))
            except ValueError:
                # silently clear invalid date (no modal)
                self.data_fim.delete(0, 'end')
                data_fim_dt = None

        self.vis_area.configure(state="normal")
        self.vis_area.delete("0.0", "end")

        if tipo == "Relatório geral de funcionários":
            rows = listar_funcionarios(1000, 0)
            self.current_report = ("geral", rows)
            lines = ["ID,Nome,Gênero,Cargo,E-mail,Salário\n"]
            for r in rows:
                lines.append(f"{r[0]},{r[1]},{r[2] or ''},{r[3] or ''},{r[4] or ''},{r[5]}\n")
            self.vis_area.insert("0.0", ''.join(lines))

        elif tipo == "Folha de pagamento":
            # total e listagem
            conn = _get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, nome, salario FROM funcionarios ORDER BY id ASC")
            rows = cur.fetchall()
            total = sum([r[2] or 0.0 for r in rows])
            media = (total / len(rows)) if rows else 0.0
            self.current_report = ("folha", rows)
            txt = [f"Folha de pagamento\nTotal: R$ {total:,.2f}\nMédia: R$ {media:,.2f}\n\nLista de funcionários:\n"]
            for r in rows:
                txt.append(f"{r[0]} - {r[1]} - R$ {r[2] or 0.0:.2f}\n")
            self.vis_area.insert("0.0", ''.join(txt))
            conn.close()

        elif tipo == "Análise de cargos":
            conn = _get_connection()
            cur = conn.cursor()
            cur.execute("SELECT cargo, COUNT(*) as cnt, AVG(salario) as avg_sal FROM funcionarios GROUP BY cargo ORDER BY cnt DESC")
            rows = cur.fetchall()
            self.current_report = ("cargos", rows)
            txt = ["Análise por cargo\n\n"]
            for r in rows:
                txt.append(f"Cargo: {r[0] or 'N/D'} - Quantidade: {r[1]} - Média salarial: R$ {r[2] or 0.0:.2f}\n")
            self.vis_area.insert("0.0", ''.join(txt))
            conn.close()

        else:
            # Turnover sem dados suficientes
            self.current_report = ("turnover", None)
            self.vis_area.insert("0.0", "Turnover: não há dados de entrada/saída no banco para calcular turnover. Adicionar colunas de admissão/desligamento primeiro.")

        self.vis_area.configure(state="disabled")

    def export_csv(self):
        if not self.current_report:
            self.controller.mostrar_aviso("Gere um relatório antes de exportar.")
            return

        kind, data = self.current_report
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        out = os.path.join(os.path.dirname(__file__) + '/../', f"relatorio_{kind}_{ts}.csv")
        try:
            if kind == 'geral' and data:
                with open(out, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'nome', 'genero', 'cargo', 'email', 'salario'])
                    for r in data:
                        writer.writerow(r)
            elif kind == 'folha' and data:
                with open(out, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['id', 'nome', 'salario'])
                    for r in data:
                        writer.writerow([r[0], r[1], r[2]])
            elif kind == 'cargos' and data:
                with open(out, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['cargo', 'quantidade', 'media_salarial'])
                    for r in data:
                        writer.writerow([r[0], r[1], r[2]])
            else:
                with open(out, 'w', newline='', encoding='utf-8') as f:
                    f.write('')
            self.controller.mostrar_aviso(f"Relatório exportado: {out}")
        except Exception as e:
            self.controller.mostrar_aviso(f"Falha ao exportar: {e}")
