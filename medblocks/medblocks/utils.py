import frappe
from frappe.utils import getdate
from dateutil.relativedelta import relativedelta

@frappe.whitelist()
def get_mrd_no(party):
    mrd_no = frappe.db.get_value("Customer", {"name": party}, "mrd_no")
    return {"mrd_no": mrd_no}
@frappe.whitelist()
def get_age(dob):
  age_str = ""
  if dob:
    born = getdate(dob)
    age = relativedelta(getdate(), born)
    age_str = str(age.years) + " year(s) " + str(age.months) + " month(s) " + str(age.days) + " day(s)"
  return {"age": age_str}
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