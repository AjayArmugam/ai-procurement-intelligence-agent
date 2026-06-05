import os

from dotenv import load_dotenv

from sqlalchemy import (
    create_engine,
    text
)

load_dotenv()

# =====================================
# Database Connection
# =====================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:

    DATABASE_URL = (
        f"postgresql://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# =====================================
# Get Invoice Status
# =====================================

def get_invoice_status(
    invoice_number
):

    query = text("""
        SELECT
            invoice_number,
            amount,
            status
        FROM invoices
        WHERE invoice_number = :invoice_number
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "invoice_number":
                invoice_number
            }
        )

        row = result.fetchone()

    if row:

        return dict(
            row._mapping
        )

    return None


# =====================================
# Get Unpaid Invoices
# =====================================

def get_unpaid_invoices():

    query = text("""
        SELECT
            invoice_number,
            amount,
            status
        FROM invoices
        WHERE status = 'UNPAID'
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query
        )

        return [
            dict(row._mapping)
            for row in result
        ]


# =====================================
# Get Vendor Details
# =====================================

def get_vendor_details(
    vendor_name
):

    query = text("""
        SELECT *
        FROM vendors
        WHERE vendor_name = :vendor_name
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "vendor_name":
                vendor_name
            }
        )

        row = result.fetchone()

    if row:

        return dict(
            row._mapping
        )

    return None


# =====================================
# Update Invoice Status
# =====================================

def update_invoice_status(
    invoice_number,
    new_status
):

    query = text("""
        UPDATE invoices
        SET status = :new_status
        WHERE invoice_number = :invoice_number
    """)

    with engine.begin() as conn:

        conn.execute(
            query,
            {
                "invoice_number":
                invoice_number,

                "new_status":
                new_status
            }
        )

    return {
        "invoice_number":
        invoice_number,

        "status":
        new_status
    }
# =====================================
# Total Pending Amount
# =====================================

def get_total_pending_amount():

    query = text("""
        SELECT
            SUM(amount)
            AS total_pending
        FROM invoices
        WHERE status = 'UNPAID'
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query
        )

        row = result.fetchone()

    return dict(
        row._mapping
    )

# =====================================
# All Unpaid Invoices
# =====================================

def get_all_unpaid_invoices():

    query = text("""
        SELECT
            invoice_number,
            amount,
            status
        FROM invoices
        WHERE status = 'UNPAID'
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query
        )

        return [
            dict(row._mapping)
            for row in result
        ]

# =====================================
# Total Approved Invoices
# =====================================

def get_total_approved_invoices():

    query = text("""
        SELECT
            COUNT(*)
            AS total_approved
        FROM invoices
        WHERE status = 'APPROVED'
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query
        )

        row = result.fetchone()

    return dict(
        row._mapping
    )

# =====================================
# Total Procurement Spend
# =====================================

def get_total_procurement_spend():

    query = text("""
        SELECT
            SUM(amount)
            AS total_spend
        FROM invoices
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query
        )

        row = result.fetchone()

    return dict(
        row._mapping
    )

# =====================================
# Top Vendor By Spend
# =====================================

def get_top_vendor_by_spend():

    query = text("""
        SELECT
            v.vendor_name,
            SUM(i.amount) AS total_spend
        FROM invoices i
        JOIN vendors v
            ON i.vendor_id = v.vendor_id
        GROUP BY v.vendor_name
        ORDER BY total_spend DESC
        LIMIT 1
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        row = result.fetchone()

    if row:

        return dict(row._mapping)

    return None

# =====================================
# Vendor Spend
# =====================================

def get_vendor_spend(vendor_name):

    query = text("""
        SELECT
            v.vendor_name,
            SUM(i.amount) AS total_spend
        FROM invoices i
        JOIN vendors v
            ON i.vendor_id = v.vendor_id
        WHERE LOWER(v.vendor_name)
            = LOWER(:vendor_name)
        GROUP BY v.vendor_name
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "vendor_name":
                vendor_name
            }
        )

        row = result.fetchone()

    if row:

        return dict(row._mapping)

    return None