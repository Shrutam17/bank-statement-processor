import csv
import os
import random

TEMPLATES = {
    "Salary": ["SALARY CREDIT {company}", "NEFT SALARY {company} MAR", "PAYROLL {company} CREDIT"],
    "Rent": ["RENT PAID TO {name}", "HOUSE RENT {name} UPI", "RENT TRANSFER {name}"],
    "Utilities": ["ELECTRICITY BILL PAYMENT", "WATER BILL BBMP", "BROADBAND BILL ACT FIBERNET", "GAS BILL INDANE"],
    "Groceries": ["BIGBASKET ORDER", "DMART PURCHASE", "GROFERS PAYMENT", "RELIANCE FRESH BILL"],
    "Food & Dining": ["SWIGGY ORDER", "ZOMATO ORDER PAYMENT", "STARBUCKS COFFEE", "DOMINOS PIZZA ORDER"],
    "Shopping": ["AMAZON PURCHASE", "FLIPKART ORDER PAYMENT", "MYNTRA SHOPPING", "AJIO ORDER"],
    "Transport": ["UBER TRIP PAYMENT", "OLA CAB PAYMENT", "FASTAG RECHARGE", "PETROL PUMP HP"],
    "Travel": ["MAKEMYTRIP FLIGHT BOOKING", "AIRBNB STAY PAYMENT", "GOIBIBO HOTEL BOOKING"],
    "Entertainment": ["NETFLIX SUBSCRIPTION", "SPOTIFY PREMIUM", "BOOKMYSHOW TICKET", "PVR CINEMAS"],
    "Healthcare": ["APOLLO PHARMACY BILL", "HOSPITAL CONSULTATION FEE", "MEDPLUS PURCHASE"],
    "Insurance": ["LIC PREMIUM PAYMENT", "INSURANCE POLICY PREMIUM"],
    "Investment": ["ZERODHA FUND TRANSFER", "MUTUAL FUND SIP", "GROWW INVESTMENT"],
    "Loan/EMI": ["HOME LOAN EMI", "CAR LOAN INSTALLMENT", "PERSONAL LOAN EMI PAYMENT"],
    "Credit Card Payment": ["CREDIT CARD BILL PAYMENT", "CC PAYMENT HDFC"],
    "Bank Charges": ["ANNUAL MAINTENANCE CHARGE", "SERVICE CHARGE DEBIT", "GST ON BANK CHARGES"],
    "Cash Withdrawal": ["ATM CASH WITHDRAWAL", "CASH WDL BRANCH"],
    "Cash Deposit": ["CASH DEPOSIT BRANCH", "CDM CASH DEPOSIT"],
    "Transfer": ["UPI TRANSFER TO {name}", "NEFT TRANSFER {name}", "IMPS FUND TRANSFER {name}"],
    "Interest": ["SAVINGS INTEREST CREDIT", "INTEREST CREDIT QUARTERLY"],
    "Tax": ["INCOME TAX PAYMENT", "TDS DEDUCTION", "ADVANCE TAX PAYMENT"],
    "Education": ["SCHOOL FEE PAYMENT", "COLLEGE FEE ONLINE", "UDEMY COURSE PAYMENT"],
    "Refund": ["AMAZON REFUND CREDIT", "ORDER REFUND", "TRANSACTION REVERSAL"],
}

COMPANIES = ["INFOSYS LTD", "TCS LTD", "WIPRO LTD", "ACCENTURE", "GLOBAL SOFT PVT LTD"]
NAMES = ["RAHUL SHARMA", "PRIYA PATEL", "AMIT KUMAR", "SNEHA REDDY", "ROHAN MEHTA"]


def generate_rows(samples_per_category=40):
    rows = []
    for category, templates in TEMPLATES.items():
        for _ in range(samples_per_category):
            template = random.choice(templates)
            description = template.format(
                company=random.choice(COMPANIES),
                name=random.choice(NAMES),
            )
            rows.append((description, category))
    random.shuffle(rows)
    return rows


def main():
    output_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "training", "labeled_transactions.csv"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    rows = generate_rows()
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["description", "category"])
        writer.writerows(rows)

    print(f"Generated {len(rows)} labeled training rows at {output_path}")


if __name__ == "__main__":
    main()
