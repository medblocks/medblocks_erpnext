import frappe
import json
from frappe.utils.response import build_response
from erpnext.selling.doctype.customer.customer import Customer
import frappe.model.rename_doc as rd
import re

phone_number_pattern = r"^\d{10}$"
email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


@frappe.whitelist()
def create_fhir_customer():
    if frappe.local.request.method != "POST":
        return return_client_error("Invalid API Method.API only accepts POST")
    data = json.loads(frappe.request.data)
    resource_type = data.get("resourceType")
    if resource_type != "Patient":
        return return_client_error("Resource is not of type Patient")
    fhir_id = data.get("id")
    if not fhir_id or not fhir_id.strip():
        return return_client_error("Resource missing Id")

    customer_name = get_human_name(data.get("name"))
    if not customer_name or not customer_name.strip():
        if not customer_name or not customer_name.strip():
            return return_client_error("Patient Name is mandatory")
    gender_hashmap = {"male": "Male", "female": "Female"}
    gender = gender_hashmap.get(data.get("gender"))
    mobile_no, email_id = get_telecom(data.get("telecom"))
    primary_address = get_address(data.get("address"))
    primary_identifier = get_primary_identifier(data.get("identifier"))
    customer_data = {
          "fhir_id": fhir_id, 
          "customer_name" : customer_name,
          "customer_type": "Individual",
          "mobile_no" : mobile_no,
          "email_id" : email_id,
          "gender": gender,
          "primary_address": primary_address
          **({"customer_uid": primary_identifier} if primary_identifier != None else {} )
       }
    status, data = upsert_customer(fhir_id, customer_data)
    
    frappe.local.response.http_status_code = status
    frappe.local.response.update(
       data
    )
    frappe.db.commit()
    return build_response("json")


def return_client_error(error):
    frappe.local.response.update({"error": error})
    frappe.local.response.http_status_code = 400
    frappe.db.commit()
    return build_response("json")


def get_human_name(human_names):
    name = None
    if not human_names or not isinstance(human_names, list):
        return name
    for human_name in human_names:
        name = human_name.get("text")
        if name and name.strip():
            return name
        given_name = human_name.get("given", [])
        if given_name:
            name = " ".join(given_name)
        if name and name.strip():
            return name
    return name


def get_telecom(telecoms):
    phone, email = None, None
    if not telecoms or not isinstance(telecoms, list):
        return phone, email
    for telecom in telecoms:
        system, value = telecom.get("system"), telecom.get("value")

        if system == "phone" and phone is None:
            phone = (
                value if value and re.match(phone_number_pattern, str(value)) else None
            )
        elif system == "email" and email is None:
            email = value if value and re.match(email_pattern, value) else None
        if phone and email:
            break
    return phone, email

def get_primary_identifier(identifiers):
    primary_identifier = None
    if not identifiers or not isinstance(identifiers, list):
        return primary_identifier
    primary_identifier = next(
    (item.get("value") for item in data if item.get("system") == frappe.local.conf.ignite_get_tasks_url),
    None
)

def get_address(addresses):
    address_text = None
    if not addresses or not isinstance(addresses, list):
        return address_text
    for address in addresses:
        address_text = address.get("text")
        if not is_not_empty_string(address_text):
            address_line = address.get("line", [])
            if address_line:
                address_text = " ".join(address_text)
        city = address.get("city")
        if is_not_empty_string(city):
            address_text = (
                address_text + f", city: {city}"
                if is_not_empty_string(address_text)
                else f"city: {city}"
            )
        district = address.get("district")
        if is_not_empty_string(district):
            address_text = (
                address_text + f", district: {district}"
                if is_not_empty_string(address_text)
                else f"district: {district}"
            )
        state = address.get("state")
        if is_not_empty_string(state):
            address_text = (
                address_text + f", state: {state}"
                if is_not_empty_string(address_text)
                else f"state: {state}"
            )
        country = address.get("country")
        if is_not_empty_string(country):
            address_text = (
                address_text + f", country: {country}"
                if is_not_empty_string(address_text)
                else f"country: {country}"
            )
        postal_code = address.get("postalCode")
        if is_not_empty_string(postal_code):
            address_text = (
                address_text + f", postalCode: {postal_code}"
                if is_not_empty_string(address_text)
                else f"postalCode: {postal_code}"
            )
        if is_not_empty_string(address_text):
            return address_text
    return address_text


def is_not_empty_string(val):
    return val and str(val).strip()


def upsert_customer(fhir_id, customer_data):
    try:
        existing_customer = frappe.db.exists("Customer", {"fhir_id": fhir_id})
        if existing_customer:
            # Fetch the document and update it
            customer_doc = frappe.get_doc("Customer", existing_customer)
            customer_doc.update(customer_data)
            customer_doc.save()
            frappe.db.commit()
            return 200, {
                "message": f"Update customer {existing_customer} successfully."
            }
        else:
            # Create a new Customer document
            customer_doc = frappe.new_doc("Customer")
            customer_doc.update({**customer_data})
            customer_doc.insert()
            frappe.db.commit()
            return 201, {
                "message": f"Created customer {customer_doc.name} successfully."
            }

    except Exception as e:
        return 500, {"error": e}
