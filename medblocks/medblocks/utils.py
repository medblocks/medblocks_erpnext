import frappe
@frappe.whitelist()
def get_mrd_no(party):
    mrd_no = frappe.db.get_value("Customer", {"name": party}, "mrd_no")
    return {"mrd_no": mrd_no}
@frappe.whitelist()
def set_mrd(doc):
    parsed_doc = frappe.parse_json(doc)
    mrd_no = get_mrd_no(parsed_doc.party)
    try:
      frappe.db.set_value("Payment Request", parsed_doc.name, 'mrd_no',mrd_no["mrd_no"], update_modified=False)
      frappe.db.commit()
    except Exception as e:
       frappe.log_error(e)
    return mrd_no