import frappe
import json
from frappe.utils.response import build_response

@frappe.whitelist()
def create_opportunity():
    if frappe.local.request.method != "POST":
        return return_client_error("Invalid API Method.API only accepts POST")
    data = json.loads(frappe.request.data)
    mrd_no = data.get("mrd_no")
    if not mrd_no:
        return return_client_error("mrd_no is mandatory")

    existing_customer = frappe.db.exists("Customer", {"mrd_no": mrd_no})
    if not existing_customer:
        return return_client_error("Missing customer with given mrd no")

    data = {
        "mrd_no": mrd_no,
        "opportunity_from": "Customer",
        "party_name": existing_customer,
        "status": "Open",
        "opportunity_type": "Surgery",
    }
    status, data = upsert_opportunity(data)

    frappe.local.response.http_status_code = status
    frappe.local.response.update(data)
    frappe.db.commit()
    return build_response("json")


def return_client_error(error):
    frappe.local.response.update({"error": error})
    frappe.local.response.http_status_code = 400
    frappe.db.commit()
    return build_response("json")

def upsert_opportunity(data):
    try:
        doc = frappe.new_doc("Opportunity")
        doc.update(data)
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return 201, {"message": f"Created Opportunity {doc.name} successfully."}
    except Exception as e:
        frappe.set_error(e, "Error Opportunity")
        return 500, {"error": e}
