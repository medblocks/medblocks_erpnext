import frappe
from frappe import _
import requests
from requests.auth import HTTPBasicAuth
import json
import uuid


@frappe.whitelist()
def get_medblocks_services_to_invoice(patient, company, encounter):
    patient = frappe.get_doc("Patient", patient)
    # encounter = frappe.get_doc("Patient Encounter", encounter)
    items_to_invoice = []
    if patient:
        validate_customer_created(patient)
        # Customer validated, build a list of billable services
        items_to_invoice += get_tasks_to_invoice(patient, company, encounter)
        return items_to_invoice


def validate_customer_created(patient):
    if not frappe.db.get_value("Patient", patient.name, "customer"):
        msg = _("Please set a Customer linked to the Patient")
        msg += " <b><a href='/app/Form/Patient/{0}'>{0}</a></b>".format(patient.name)
        frappe.throw(msg, title=_("Customer Not Found"))


def get_tasks_to_invoice(patient, company, encounter):
    tasks_to_invoice = []
    ignite_url = frappe.local.conf.ignite_get_tasks_url
    token_url = frappe.local.conf.token_endpoint
    client_id = frappe.local.conf.client_id
    client_secret = frappe.local.conf.client_secret
    mb_tasks = []
    try:
        response_auth = requests.post(token_url, 
                         auth=HTTPBasicAuth(client_id, client_secret),
                         data={'grant_type': 'client_credentials'})
        access_token = response_auth.json().get('access_token')
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {access_token}'
        }
        patient_id = generate_uuid(patient.name)
        print(patient_id)
        ignite_url = ignite_url + "/" + patient_id
        # data = {"patient": patient.name, "encounter": encounter.name}
        res = requests.get(ignite_url, headers=headers)
        print(res.text)
        mb_tasks = res.json()
        if not isinstance(mb_tasks, list): mb_tasks = []
    except Exception as e:
        msg = _("Error getting Medblocks task")
        msg += " <b><a href='{0}'>{1}</a></b>".format(ignite_url, patient.name)
        frappe.throw(msg, title=_("Error getting Medblocks task"))
    
    for task in mb_tasks:
        print(task, mb_tasks)
        # Create Item in Stock Items
        if not frappe.db.exists("Item", task["item_code"]):
            Item = frappe.new_doc("Item")
            Item.item_code = task["item_code"]
            Item.item_name = task["item_code"]
            Item.description = task.get("description", task["item_code"])
            Item.item_group = "Drug" if task.get("type") == "medication" else "Medblocks"
            Item.standard_rate = 0.0
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
            Item.flags.ignore_manadatory = True
            Item.flags.ignore_permissions = True
            Item.insert()
            Item.save()
            ItemPrice = frappe.new_doc("Item Price")
            ItemPrice.item_code = task["item_code"]
            ItemPrice.price_list = "Standard Selling"
            ItemPrice.price_list_rate = 0.0
            ItemPrice.flags.ignore_manadatory = True
            ItemPrice.flags.ignore_permissions = True
            ItemPrice.insert()
            ItemPrice.save()
        amount = frappe.db.get_value(
            "Item Price", {"item_code": task["item_code"]}, "price_list_rate"
        )
        amount = amount if amount else 0
        tasks_to_invoice.append(
            {
                "reference_type": "MB_Task/" + str(task["id"]),
                "service": task["item_code"],
                "rate": amount,
                "quantity": task.get("quantity") if task.get("quantity") or task.get("quantity") ==0 else 1 
            }
        )
        # Consultation Appointments, should check fee validity
    return tasks_to_invoice


def manage_invoice_submit_cancel(doc, method):
    if not doc.patient:
        return

    
    if doc.items:
        if method == "on_submit":
            post_task_to_ignite(doc, "billed")

        if method == "on_cancel":
           post_task_to_ignite(doc, "cancelled")

        
def manage_payment_submit_cancel(doc, method):
    if doc.references:
        for refrence in doc.references:
            if refrence.reference_doctype and refrence.reference_doctype == "Sales Invoice":
                salesDoc = frappe.get_doc('Sales Invoice', refrence.reference_name )
                if not salesDoc.patient:
                    return
                if salesDoc.items:
                    if method == "on_submit":
                        post_task_to_ignite(salesDoc, "paid")

                    if method == "on_cancel":
                        post_task_to_ignite(salesDoc, "billed")

def generate_uuid(name):
    """Generate a unique identifier for FHIR server

    Args:
        name str : Name of the patient as per the patient

    Returns:
        str : UUIDv5 with URL Namespace
    """
    namespace = uuid.NAMESPACE_URL
    unique_id = uuid.uuid5(namespace, str(name))
    return str(unique_id)

def post_task_to_ignite(doc, task_status):
    MB_Tasks = []
    if task_status =="billed":
        for item in doc.items:
            if item.item_name and item.item_name.startswith("MB_Task/"):
                task_id = item.item_name.split("/")[1]
                task_item = {"id": task_id, "sales_order": doc.name, "status": "billed"}
                MB_Tasks.append(task_item)
    if task_status =="cancelled":
        for item in doc.items:
            if item.item_name and item.item_name.startswith("MB_Task/"):
                task_id = item.item_name.split("/")[1]
                task_item = {"id": task_id, "sales_order": None, "status": "init"}
                MB_Tasks.append(task_item)
    if task_status =="paid":
        for item in doc.items:
            if item.item_name and item.item_name.startswith("MB_Task/"):
                task_id = item.item_name.split("/")[1]
                task_item = {"id": task_id, "sales_order": doc.name, "status": "paid"}
                MB_Tasks.append(task_item)
    if task_status =="unpaid":
        for item in doc.items:
            if item.item_name and item.item_name.startswith("MB_Task/"):
                task_id = item.item_name.split("/")[1]
                task_item = {"id": task_id, "sales_order": doc.name, "status": "billed"}
                MB_Tasks.append(task_item)
    if (len(MB_Tasks)) > 0:
        ignite_url = frappe.local.conf.ignite_update_tasks_url
        token_url = frappe.local.conf.token_endpoint
        client_id = frappe.local.conf.client_id
        client_secret = frappe.local.conf.client_secret
        patient = frappe.get_doc("Patient", doc.patient)
        try:
            response_auth = requests.post(token_url, 
                            auth=HTTPBasicAuth(client_id, client_secret),
                            data={'grant_type': 'client_credentials'})
            access_token = response_auth.json().get('access_token')
            headers = {
                "Content-Type": "application/json",
                'Authorization': f'Bearer {access_token}'
            }
            patient_uid = generate_uuid(patient.name)
            ignite_url = ignite_url + "/" + patient_uid
            res = requests.put(
                ignite_url, headers=headers, data=json.dumps(MB_Tasks)
            )
            res.json()
            print(res.text)
        except Exception as e:
            msg = _("Error Updating Medblocks task")
            msg += " <b><a href='{0}'>{1}</a></b>".format(ignite_url, patient.name)
            frappe.throw(msg, title=_("Error Updating Medblocks task"))