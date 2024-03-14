import frappe
from frappe import _
import requests
import json


@frappe.whitelist()
def get_ignite_services_to_invoice(patient, company):
    patient = frappe.get_doc("Patient", patient)
    items_to_invoice = []
    if patient:
        validate_customer_created(patient)
        # Customer validated, build a list of billable services
        items_to_invoice += get_tasks_to_invoice(patient, company)
        return items_to_invoice


def validate_customer_created(patient):
    if not frappe.db.get_value("Patient", patient.name, "customer"):
        msg = _("Please set a Customer linked to the Patient")
        msg += " <b><a href='/app/Form/Patient/{0}'>{0}</a></b>".format(patient.name)
        frappe.throw(msg, title=_("Customer Not Found"))


def get_tasks_to_invoice(patient, company):
    tasks_to_invoice = []
    ignite_url = frappe.local.conf.ignite_get_tasks_url
    mb_tasks = []
    try:
        ignite_url = ignite_url + "/" + patient.name
        headers = {"Content-Type": "application/json"}
        res = requests.get(ignite_url, headers=headers)
        mb_tasks = res.json()
    except Exception as e:
        msg = _("Error getting Medblocks task")
        msg += " <b><a href='{0}'>{1}</a></b>".format(ignite_url, patient.name)
        frappe.throw(msg, title=_("Error getting Medblocks task"))
    for task in mb_tasks:

        # Create Item in Stock Items
        if not frappe.db.exists("Item", task["task_name"]):
            Item = frappe.new_doc("Item")
            Item.item_code = task["task_name"]
            Item.item_name = task["task_name"]
            Item.item_group = "Medblocks"
            Item.stock_uom = "Nos"
            Item.disabled = 0
            Item.allow_alternative_item = 0
            Item.is_stock_item = 0
            Item.has_variants = 0
            Item.include_item_in_manufacturing = 0
            Item.opening_stock = 0
            Item.valuation_rate = 0
            Item.standard_rate = 0
            Item.is_fixed_asset = 0
            Item.auto_create_assets = 0
            Item.is_grouped_asset = 0
            Item.insert()
        tasks_to_invoice.append(
            {
                "reference_type": "MB_Tasks",
                "service": task["task_name"],
                "rate": task["amount"],
            }
        )
        # Consultation Appointments, should check fee validity
    return tasks_to_invoice


def manage_invoice_submit_cancel(doc, method):
    if not doc.patient:
        return

    if doc.items:
        if method == "on_submit":
            for item in doc.items:
                if item.reference_dt == "Ignite Task":
                    frappe.db.set_value("MB_Tasks", item.reference_dn, "docStatus", 1)

        if method == "on_cancel":
            for item in doc.items:
                if item.reference_dt == "Ignite Task":
                    frappe.db.set_value(
                        "MB_Tasks", item.reference_dn, "status", "Cancelled"
                    )
