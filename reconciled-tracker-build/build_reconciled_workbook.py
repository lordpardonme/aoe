import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "reconciled-tracker-build"
OUT = BUILD / "master_job_tracker_reconciled.xlsx"

FILES = [
    ("Master Leads", BUILD / "master_leads.tsv"),
    ("Agencies", BUILD / "agencies.tsv"),
    ("Direct Employers", BUILD / "direct_employers.tsv"),
    ("Forms", BUILD / "forms.tsv"),
    ("LinkedIn Search", BUILD / "linkedin_search.tsv"),
    ("Phone WhatsApp", BUILD / "phone_whatsapp.tsv"),
]

HEADER_FILL = PatternFill("solid", fgColor="E5E7EB")
DARK_FILL = PatternFill("solid", fgColor="111827")
WHITE_FONT = Font(color="FFFFFF", bold=True)
HEADER_FONT = Font(color="111827", bold=True)
THIN_GRAY = Side(style="thin", color="D1D5DB")
BORDER = Border(bottom=THIN_GRAY)

COLUMN_WIDTHS = {
    "A": 18, "B": 18, "C": 26, "D": 34, "E": 22, "F": 32, "G": 34,
    "H": 18, "I": 28, "J": 18, "K": 15, "L": 15, "M": 15, "N": 18,
    "O": 14, "P": 18, "Q": 32, "R": 28, "S": 48, "T": 42, "U": 24, "V": 24,
}


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f, delimiter="\t"))


def style_table(ws):
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    max_row = ws.max_row
    max_col = ws.max_column
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    for col_idx in range(1, max_col + 1):
        letter = get_column_letter(col_idx)
        ws.column_dimensions[letter].width = COLUMN_WIDTHS.get(letter, 20)
    for row in ws.iter_rows(min_row=2, max_row=max_row, max_col=max_col):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
    ws.sheet_view.showGridLines = True

    # Keep status fields controlled without making the workbook brittle.
    validations = {
        "B": '"Agency,Direct Employer,Form,LinkedIn Search,Phone / WhatsApp Lead"',
        "J": '"To Contact,Applied,Followed Up,Needs Review,Delivery Failed,Rejected / Appeal Sent,Networking"',
        "N": '"No Reply,Replied,Replied / Active Process,Bounced,Rejected,Interview"',
        "O": '"High,Medium,Low,Unknown"',
        "P": '"Yes,No"',
    }
    for col, formula in validations.items():
        dv = DataValidation(type="list", formula1=formula, allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col}2:{col}{max(max_row, 2000)}")

    if max_row >= 2:
        status_col = "J"
        reply_col = "N"
        review_col = "P"
        ws.conditional_formatting.add(
            f"{status_col}2:{status_col}{max_row}",
            FormulaRule(formula=[f'ISNUMBER(SEARCH("Applied",{status_col}2))'], fill=PatternFill("solid", fgColor="DCFCE7")),
        )
        ws.conditional_formatting.add(
            f"{status_col}2:{status_col}{max_row}",
            FormulaRule(formula=[f'ISNUMBER(SEARCH("Delivery Failed",{status_col}2))'], fill=PatternFill("solid", fgColor="FEE2E2")),
        )
        ws.conditional_formatting.add(
            f"{reply_col}2:{reply_col}{max_row}",
            FormulaRule(formula=[f'ISNUMBER(SEARCH("Replied",{reply_col}2))'], fill=PatternFill("solid", fgColor="DBEAFE")),
        )
        ws.conditional_formatting.add(
            f"{review_col}2:{review_col}{max_row}",
            CellIsRule(operator="equal", formula=['"Yes"'], fill=PatternFill("solid", fgColor="FEF3C7")),
        )


def add_table_sheet(wb, name, path):
    ws = wb.create_sheet(name)
    rows = read_tsv(path)
    for row in rows:
        ws.append(row)
    style_table(ws)
    return ws


def add_dashboard(wb):
    ws = wb.create_sheet("Dashboard")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Job Tracker Dashboard"
    ws["A1"].font = Font(size=18, bold=True, color="111827")
    ws["A2"] = "Formula-driven summary from the Master Leads tab."
    ws["A2"].font = Font(size=10, color="4B5563")

    metrics = [
        ("Master leads", '=COUNTA(\'Master Leads\'!C2:C1048576)'),
        ("Unique email-bearing rows", '=COUNTIF(\'Master Leads\'!G2:G1048576,"*@*")'),
        ("Agencies", '=COUNTIF(\'Master Leads\'!B2:B1048576,"Agency")'),
        ("Direct employers", '=COUNTIF(\'Master Leads\'!B2:B1048576,"Direct Employer")'),
        ("Forms", '=COUNTIF(\'Master Leads\'!B2:B1048576,"Form")'),
        ("LinkedIn / search rows", '=COUNTA(\'LinkedIn Search\'!C2:C1048576)'),
        ("Phone / WhatsApp rows", '=COUNTA(\'Phone WhatsApp\'!C2:C1048576)'),
        ("Applied", '=COUNTIF(\'Master Leads\'!J2:J1048576,"Applied")'),
        ("Followed up", '=COUNTIF(\'Master Leads\'!J2:J1048576,"Followed Up")'),
        ("Needs review", '=COUNTIF(\'Master Leads\'!P2:P1048576,"Yes")'),
        ("Replies", '=COUNTIF(\'Master Leads\'!N2:N1048576,"Replied*")'),
        ("Bounced", '=COUNTIF(\'Master Leads\'!N2:N1048576,"Bounced")'),
        ("Rejected", '=COUNTIF(\'Master Leads\'!N2:N1048576,"Rejected")+COUNTIF(\'Master Leads\'!J2:J1048576,"Rejected*")'),
        ("Follow-ups due", '=COUNTIFS(\'Master Leads\'!M2:M1048576,"<="&TODAY(),\'Master Leads\'!M2:M1048576,"<>",\'Master Leads\'!J2:J1048576,"<>Rejected*")'),
        ("Last Gmail scan", "2026-06-07"),
    ]
    start = 4
    ws.cell(start, 1, "Metric")
    ws.cell(start, 2, "Value")
    for cell in ws[start]:
        cell.fill = DARK_FILL
        cell.font = WHITE_FONT
        cell.alignment = Alignment(horizontal="center")
    for idx, (label, value) in enumerate(metrics, start + 1):
        ws.cell(idx, 1, label)
        ws.cell(idx, 2, value)
        ws.cell(idx, 1).alignment = Alignment(vertical="top")
        ws.cell(idx, 2).alignment = Alignment(vertical="top")
        ws.cell(idx, 1).border = BORDER
        ws.cell(idx, 2).border = BORDER
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 20
    ws.freeze_panes = "A5"


def main():
    wb = Workbook()
    default = wb.active
    wb.remove(default)
    for name, path in FILES:
        add_table_sheet(wb, name, path)
    add_dashboard(wb)
    wb.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
