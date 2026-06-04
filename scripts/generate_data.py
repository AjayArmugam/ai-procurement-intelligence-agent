from faker import Faker
import random
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

fake = Faker()

# Create docs folder if it doesn't exist
os.makedirs("docs", exist_ok=True)

# -----------------------------
# Generate Vendors
# -----------------------------

vendors = []

for i in range(1, 21):

    vendors.append({
        "vendor_id": i,
        "vendor_name": fake.company(),
        "email": fake.email(),
        "phone": fake.phone_number()
    })

print(f"Generated {len(vendors)} Vendors")


# -----------------------------
# Procurement Categories
# -----------------------------

departments = [
    "Procurement",
    "Manufacturing",
    "Operations",
    "Healthcare",
    "IT"
]

payment_terms_options = [
    "Net 30",
    "Net 45",
    "Net 60"
]

items = [
    "Industrial Sensors",
    "Medical Equipment",
    "Software Licenses",
    "Cloud Infrastructure",
    "Maintenance Services",
    "Networking Equipment",
    "Security Cameras",
    "Factory Automation Components",
    "Data Storage Systems",
    "Office Hardware"
]


# -----------------------------
# Generate Invoice PDFs
# -----------------------------

for i in range(1, 101):

    vendor = random.choice(vendors)

    invoice_number = f"INV-{1000+i}"

    po_number = f"PO-{2000+i}"

    department = random.choice(departments)

    payment_terms = random.choice(
        payment_terms_options
    )

    item = random.choice(items)

    quantity = random.randint(1, 50)

    amount = random.randint(
        5000,
        100000
    )

    status = random.choice([
        "PAID",
        "UNPAID"
    ])

    description = (
        f"Purchase of {item} "
        f"for organizational operations."
    )

    pdf_path = f"docs/{invoice_number}.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "<b>PROCUREMENT INVOICE</b>",
            styles["Title"]
        ),

        Spacer(1, 12),

        Paragraph(
            f"<b>Invoice Number:</b> {invoice_number}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Purchase Order:</b> {po_number}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Vendor:</b> {vendor['vendor_name']}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Department:</b> {department}",
            styles["Normal"]
        ),

        Paragraph(
            "<b>Invoice Date:</b> 2026-05-01",
            styles["Normal"]
        ),

        Paragraph(
            "<b>Due Date:</b> 2026-06-01",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Payment Terms:</b> {payment_terms}",
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            "<b>ITEM DETAILS</b>",
            styles["Heading2"]
        ),

        Paragraph(
            f"<b>Item:</b> {item}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Quantity:</b> {quantity}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Amount:</b> ₹{amount}",
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            "<b>DESCRIPTION</b>",
            styles["Heading2"]
        ),

        Paragraph(
            description,
            styles["Normal"]
        ),

        Spacer(1, 10),

        Paragraph(
            f"<b>Status:</b> {status}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Vendor Email:</b> {vendor['email']}",
            styles["Normal"]
        ),

        Paragraph(
            f"<b>Vendor Phone:</b> {vendor['phone']}",
            styles["Normal"]
        )
    ]

    doc.build(content)

print("Generated 100 Enterprise Invoice PDFs Successfully!")