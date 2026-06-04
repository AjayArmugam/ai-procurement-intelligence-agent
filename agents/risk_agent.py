from database.postgres import (
    get_total_pending_amount,
    get_top_vendor_by_spend,
    get_all_unpaid_invoices,
    get_total_procurement_spend
)

def risk_agent(state):

    print("Entering Risk Agent")

    pending = (
        get_total_pending_amount()
    )

    vendor = (
        get_top_vendor_by_spend()
    )

    unpaid = (
        get_all_unpaid_invoices()
    )

    spend = (
        get_total_procurement_spend()
    )

    state["context"] = f"""
Total Procurement Spend:
{spend}

Pending Amount:
{pending}

Top Vendor:
{vendor}

Unpaid Invoices:
{unpaid}
"""

    return state