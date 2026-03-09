import csv
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

class ReportsService:
    def __init__(self, repo):
        self.repo = repo

    def get_dashboard_summary(self):
        return self.repo.dashboard_summary()

    def generate_dashboard_csv(self) -> str:
        data = self.get_dashboard_summary()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["Campo", "Valor"])
        writer.writerow(["Tareas totales", data["tareas_total"]])
        writer.writerow(["Tareas pendientes", data["tareas_pendientes"]])
        writer.writerow(["Tareas en progreso", data["tareas_en_progreso"]])
        writer.writerow(["Tareas completadas", data["tareas_completadas"]])
        writer.writerow(["Tareas canceladas", data["tareas_canceladas"]])
        writer.writerow(["Tareas vencidas", data["tareas_vencidas"]])
        writer.writerow(["Recursos totales", data["recursos_total"]])
        writer.writerow(["Recursos sin stock", data["recursos_sin_stock"]])
        writer.writerow(["Recursos en mantenimiento", data["recursos_en_mantenimiento"]])

        return output.getvalue()
    
    def generate_dashboard_excel(self) -> bytes:
        data = self.get_dashboard_summary()

        wb = Workbook()
        ws = wb.active
        ws.title = "Dashboard"

        # Título
        ws["A1"] = "Reporte Dashboard"
        ws["A1"].font = Font(bold=True, size=14)
        ws.merge_cells("A1:B1")
        ws["A1"].alignment = Alignment(horizontal="center")

        # Encabezados
        ws["A3"] = "Campo"
        ws["B3"] = "Valor"

        header_fill = PatternFill("solid", fgColor="D9EAD3")
        header_font = Font(bold=True)

        ws["A3"].fill = header_fill
        ws["B3"].fill = header_fill
        ws["A3"].font = header_font
        ws["B3"].font = header_font

        rows = [
            ("Tareas totales", data["tareas_total"]),
            ("Tareas pendientes", data["tareas_pendientes"]),
            ("Tareas en progreso", data["tareas_en_progreso"]),
            ("Tareas completadas", data["tareas_completadas"]),
            ("Tareas canceladas", data["tareas_canceladas"]),
            ("Tareas vencidas", data["tareas_vencidas"]),
            ("Recursos totales", data["recursos_total"]),
            ("Recursos sin stock", data["recursos_sin_stock"]),
            ("Recursos en mantenimiento", data["recursos_en_mantenimiento"]),
        ]

        start_row = 4
        for i, (campo, valor) in enumerate(rows, start=start_row):
            ws[f"A{i}"] = campo
            ws[f"B{i}"] = valor

        # Anchos de columna
        ws.column_dimensions["A"].width = 30
        ws.column_dimensions["B"].width = 15

        # Guardar en memoria
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return output.getvalue()