import frappe

def execute(filters=None):
    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 260},
        {"label": "Latest Incoming Date", "fieldname": "latest_posting_date", "fieldtype": "Date", "width": 130},
        {"label": "Latest Incoming Rate", "fieldname": "latest_incoming_rate", "fieldtype": "Currency", "width": 150},
    ]

    data = frappe.db.sql(
        """
        SELECT
            i.name AS item_code,
            i.item_name,

            DATE_FORMAT(sle.posting_date, '%d-%m-%Y') AS latest_posting_date,
            sle.incoming_rate AS latest_incoming_rate

        FROM `tabItem` i

        LEFT JOIN `tabStock Ledger Entry` sle
            ON sle.name = (
                SELECT s2.name
                FROM `tabStock Ledger Entry` s2
                WHERE s2.item_code = i.name
                  AND s2.actual_qty > 0
                  AND s2.docstatus < 2
                  AND s2.is_cancelled = 0
                ORDER BY s2.posting_date DESC, s2.posting_time DESC, s2.creation DESC
                LIMIT 1
            )

        ORDER BY i.name ASC
        """,
        as_dict=True,
    )

    return columns, data
