import os
import random
import sys
from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pdf2image import convert_from_path  # noqa: E402
from PIL import Image  # noqa: E402

DESCRIPTIONS = [
    "SALARY CREDIT INFOSYS LTD",
    "SWIGGY ORDER PAYMENT",
    "AMAZON PURCHASE",
    "ATM CASH WITHDRAWAL",
    "ELECTRICITY BILL PAYMENT",
    "UPI TRANSFER TO RAHUL SHARMA",
    "NETFLIX SUBSCRIPTION",
    "RENT PAID TO PRIYA PATEL",
    "ZERODHA FUND TRANSFER",
    "HOME LOAN EMI",
    "BIGBASKET ORDER",
    "UBER TRIP PAYMENT",
    "CREDIT CARD BILL PAYMENT",
    "INTEREST CREDIT QUARTERLY",
    "CASH DEPOSIT BRANCH",
]


def generate_transactions(count=25, opening_balance=50000.0):
    transactions = []
    balance = opening_balance
    current_date = date(2026, 3, 1)

    for _ in range(count):
        current_date += timedelta(days=random.randint(0, 2))
        description = random.choice(DESCRIPTIONS)
        is_credit = "CREDIT" in description or "SALARY" in description or "DEPOSIT" in description or "REFUND" in description
        amount = round(random.uniform(200, 25000), 2)

        debit = 0.0 if is_credit else amount
        credit = amount if is_credit else 0.0
        balance = balance + credit - debit

        transactions.append(
            {
                "date": current_date.strftime("%d/%m/%Y"),
                "description": description,
                "debit": f"{debit:,.2f}" if debit else "",
                "credit": f"{credit:,.2f}" if credit else "",
                "balance": f"{balance:,.2f}",
            }
        )
    return transactions


def build_text_based_pdf(output_path, account_number="123456789012", ifsc="HDFC0001234"):
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Sunrise National Bank", styles["Title"]))
    elements.append(Paragraph("Account Statement", styles["Heading2"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("Account Holder Name: RAHUL SHARMA", styles["Normal"]))
    elements.append(Paragraph(f"Account No: {account_number}", styles["Normal"]))
    elements.append(Paragraph(f"IFSC: {ifsc}", styles["Normal"]))
    elements.append(Paragraph("Branch: MG Road, Bengaluru", styles["Normal"]))
    elements.append(Spacer(1, 16))

    transactions = generate_transactions()
    table_data = [["Date", "Description", "Debit", "Credit", "Balance"]]
    for txn in transactions:
        table_data.append([txn["date"], txn["description"], txn["debit"], txn["credit"], txn["balance"]])

    table = Table(table_data, colWidths=[65, 190, 70, 70, 80])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    elements.append(table)
    doc.build(elements)
    return output_path


def build_image_based_pdf(text_pdf_path, output_path, dpi=300):
    images = convert_from_path(text_pdf_path, dpi=dpi)
    rendered_images = []
    for image in images:
        rgb_image = image.convert("RGB")
        rendered_images.append(rgb_image)

    rendered_images[0].save(
        output_path, save_all=True, append_images=rendered_images[1:], format="PDF"
    )
    return output_path


def main():
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_pdfs")
    os.makedirs(sample_dir, exist_ok=True)

    text_pdf_path = os.path.join(sample_dir, "sample_statement_text_based.pdf")
    build_text_based_pdf(text_pdf_path)
    print(f"Generated text-based sample PDF: {text_pdf_path}")

    second_text_pdf = os.path.join(sample_dir, "sample_statement_text_based_2.pdf")
    build_text_based_pdf(second_text_pdf, account_number="987654321098", ifsc="ICIC0009876")
    print(f"Generated text-based sample PDF: {second_text_pdf}")

    scanned_pdf_path = os.path.join(sample_dir, "sample_statement_scanned.pdf")
    build_image_based_pdf(text_pdf_path, scanned_pdf_path)
    print(f"Generated image-based/scanned sample PDF: {scanned_pdf_path}")


if __name__ == "__main__":
    main()
