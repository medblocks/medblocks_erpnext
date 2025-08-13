import frappe
import json
from frappe.utils.response import build_response
from frappe.utils import getdate
# from types import dict, str
from dateutil.relativedelta import relativedelta
import re

phone_number_pattern = r'^\+?(\d{1,14}(-\d{1,14})*)$'
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
        return return_client_error("Patient Name is mandatory")

    gender_hashmap = {"male": "Male", "female": "Female"}
    gender = gender_hashmap.get(data.get("gender"))

    mobile_nos, email_ids = get_telecom(data.get("telecom"))
    primary_address = get_address(data.get("address"))
    primary_identifier = get_primary_identifier(data.get("identifier"))
    dob = data.get("birthDate")
    relation_name, relation_type = get_relation(data.get("contact"))
    customer_data = {
        "fhir_id": fhir_id,
        "customer_name": customer_name,
        "customer_type": "Individual",
        "gender": gender,
        "primary_address": primary_address,
        "from_ignite": 1,
        "dob": dob,
        "age": get_age(dob),
        "relation_name":relation_name,
        "relation_type": relation_type,
        **({"mrd_no": primary_identifier} if primary_identifier != None else {}),
    }
    contact_data = {
        "full_name": customer_name,
        "mobile_nos": mobile_nos,
        "email_ids": email_ids,
        "gender": gender,
        "mrd_number": primary_identifier
    }
    status, data = upsert_customer(fhir_id, customer_data, contact_data)

    frappe.local.response.http_status_code = status
    frappe.local.response.update(data)
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

def get_age(dob):
  age_str = ""
  if dob:
    born = getdate(dob)
    age = relativedelta(getdate(), born)
    age_str = str(age.years) + " year(s) " + str(age.months) + " month(s) " + str(age.days) + " day(s)"
  return age_str
def get_telecom(telecoms):
    phone, email = [], []
    if not telecoms or not isinstance(telecoms, list):
        return phone, email
    patterns = {
        "phone": (phone_number_pattern, phone),
        "email": (email_pattern, email),
    }
    for telecom in telecoms:
        system, value = telecom.get("system"), telecom.get("value")
        if system in patterns and value and re.match(patterns[system][0], str(value)):
         patterns[system][1].append(value)
    return patterns["phone"][1], patterns["email"][1]

def get_relation(contacts):
    relations = contacts[0]["relationship"] if contacts and isinstance(contacts[0], dict) and "relationship" in contacts[0] else None
    relation_name, relation_type = "", ""
    relation_name = relations[0]["text"] if relations and isinstance(relations[0], dict) and "text" in relations[0] else None
    relation_type = (
        relations[0]["coding"][0]["code"]
        if relations and isinstance(relations[0], dict) and "coding" in relations[0] and isinstance(relations[0]["coding"], list) and relations[0]["coding"]
        else None
    )
    return relation_name, relation_type
    


def get_primary_identifier(identifiers):
    primary_identifier = None
    if not identifiers or not isinstance(identifiers, list):
        return primary_identifier
    primary_identifier = next(
        (
            item.get("value")
            for item in identifiers
            if item.get("system") == frappe.local.conf.patient_primary_identifier_system
        ),
        None,
    )
    return primary_identifier


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


def upsert_customer(fhir_id, customer_data, contact_data):
    try:
        existing_customer = frappe.db.exists("Customer", {"fhir_id": fhir_id})
        if existing_customer:
            customer_doc = frappe.get_doc("Customer", existing_customer)

            primary_contact = update_contact(customer_doc.customer_primary_contact, contact_data)
            customer_data.update({
                "customer_primary_contact": primary_contact,
            })
            customer_doc.update(customer_data)
            customer_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return 200, {
                "message": f"Update customer {existing_customer} successfully."
            }
        else:
            # Create a new Customer document
            customer_doc = frappe.new_doc("Customer")
            primary_contact = update_contact(customer_doc.customer_primary_contact, contact_data)
            customer_data.update({
                "customer_primary_contact": primary_contact,
            })
            customer_doc.update(customer_data)
            customer_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return 201, {
                "message": f"Created customer {customer_doc.name} successfully."
            }
    except Exception as e:
        frappe.set_error(e, "Error fhir customer")
        return 500, {"error": e}


def update_contact(contact_name, contact_data):
    try:
        first, middle, last = parse_full_name(contact_data.get("full_name"))
        new_phone_nos = []
        for phone_no in contact_data["mobile_nos"]:
                new_phone_nos.append({
                    "phone": phone_no,
					'from_fhir': 1
                })
        new_email_ids = []
        for email in contact_data["email_ids"]:
                new_email_ids.append({
                    "email_id": email,
					'from_fhir': 1
                })
        if contact_name is not None:
            contact_doc = frappe.get_doc("Contact", contact_name)
            existing_emails = contact_doc.email_ids
            filtered_emails = [email for email in existing_emails if email.from_fhir != 1]
            if len(new_email_ids) > 0 and not any(email.is_primary == 1 for email in filtered_emails):
                new_email_ids[0]["is_primary"] = 1
            email_ids = [*filtered_emails,*new_email_ids]
            existing_phone_nos = contact_doc.phone_nos
            filtered_phone_nos = [phone_no for phone_no in existing_phone_nos if phone_no.from_fhir != 1]
            if len(new_phone_nos) > 0 and not any(phone.is_primary_mobile_no == 1 for phone in filtered_phone_nos):
                new_phone_nos[0]["is_primary_mobile_no"] = 1
            phone_nos = [*filtered_phone_nos,*new_phone_nos]
            contact_doc.update({
                "first_name": first,
                "middle_name": middle,
                "last_name": last,
                "gender": contact_data.get("gender"),
                "email_ids": email_ids,
                "phone_nos": phone_nos,
                "mrd_no": contact_data.get("mrd_no")
            })
            contact_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return contact_name
        else:
            customer_doc = frappe.new_doc("Contact")
            if len(new_email_ids) > 0 :
                new_email_ids[0]["is_primary"] = 1
            if len(new_phone_nos) > 0 :
                new_phone_nos[0]["is_primary_mobile_no"] = 1
            customer_doc.update({
                "first_name": first,
                "middle_name": middle,
                "last_name": last,
                "gender": contact_data.get("gender"),
                "email_ids": new_email_ids,
                "phone_nos": new_phone_nos,
                "mrd_no": contact_data.get("mrd_no")
            })
            customer_doc.insert(ignore_permissions=True)
            contact_name = customer_doc.name
            frappe.db.commit()
            return contact_name

    except Exception as e:
        frappe.set_error(e, "Error creating fhir contact")
        return contact_name


def parse_full_name(full_name: str) -> tuple[str, str | None, str | None]:
    """Parse full name into first name, middle name and last name"""
    names = full_name.split()
    first_name = names[0]
    middle_name = " ".join(names[1:-1]) if len(names) > 2 else None
    last_name = names[-1] if len(names) > 1 else None

    return first_name, middle_name, last_name
