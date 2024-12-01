medblocks_section_break = {
    "fieldname": "medblocks_section_break",
    "fieldtype": "Section Break",
    "label": "Medblocks",
}
CUSTOMER_CUSTOM_FIELD_LIST = [
            medblocks_section_break,
            {
                "fieldname": "fhir_id",
                "fieldtype": "Data",
                "hidden": 1,
                "label": "Fhir Id",
            },
            {
                "fieldname": "mrd_no",
                "label": "MRD No",
                "fieldtype": "Data",
                "in_list_view": 1,
                "allow_in_quick_entry": 1,
                "in_standard_filter": 1,
                "in_global_search": 1,
            },
            {
                "fieldname": "from_ignite",
                "label": "From ignite",
                "fieldtype": "Check",
                "depends_on": "eval:doc.fhir_id!=null",
                "read_only": 1,
                "default": "0",
            },
]
CONTACT_CUSTOM_FIELD_LIST = [
    medblocks_section_break,
    {
                "fieldname": "mrd_no",
                "label": "MRD No",
                "fieldtype": "Data",
                "in_list_view": 1,
                "in_standard_filter": 1,
                "in_global_search": 1,
            },
]
CONTACT_EMAIL_CUSTOM_FIELD_LIST = [
            medblocks_section_break,
            {
                "fieldname": "from_fhir",
                "label": "From Fhir",
                "fieldtype": "Check",
                "read_only": 1,
                "default": "0",
            },
        ]

CONTACT_PHONE_CUSTOM_FIELD_LIST = [
            medblocks_section_break,
            {
                "fieldname": "from_fhir",
                "label": "From Fhir",
                "fieldtype": "Check",
                "read_only": 1,
                "default": "0",
            },
        ]
SALES_INVOICE_CUSTOM_FIELD_LIST = [
    {
        "fetch_from": "customer.mrd_no",
        "fieldname": "mrd_no",
        "fieldtype": "Small Text",
        "in_filter": 1,
        "in_global_search": 1,
        "in_list_view": 1,
        "in_standard_filter": 1,
        "label": "MRD No",
        "depends_on": "customer",
        "insert_after": "customer_name",
    }
]
PAYMENT_ENTRY_CUSTOM_FIELD_LIST = [
    {
        "fieldname": "mrd_no",
        "fieldtype": "Data",
        "in_filter": 1,
        "in_global_search": 1,
        "in_list_view": 1,
        "in_standard_filter": 1,
        "label": "MRD No",
        "depends_on": "eval:doc.party_type=='Customer' && doc.party",
        "insert_after": "party_name",
    }
]
PAYMENT_REQUEST_CUSTOM_FIELD_LIST = [
    {
        "fieldname": "mrd_no",
        "fieldtype": "Data",
        "in_filter": 1,
        "in_global_search": 1,
        "in_list_view": 1,
        "in_standard_filter": 1,
        "label": "MRD No",
        "depends_on": "eval:doc.party_type=='Customer' && doc.party",
        "insert_after": "party_name",
    }
]


def generate_custom_field_tuple(dt, custom_list):
    return (dt, list(map(lambda x, doctype=dt: {**x, "dt": doctype}, custom_list)))


MEDBLOCKS_CUSTOM_FIELDS = [
    generate_custom_field_tuple("Customer", CUSTOMER_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Contact", CONTACT_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Contact Email", CONTACT_EMAIL_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Contact Phone", CONTACT_PHONE_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Sales Invoice", SALES_INVOICE_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Payment Entry", PAYMENT_ENTRY_CUSTOM_FIELD_LIST),
    generate_custom_field_tuple("Payment Request", PAYMENT_REQUEST_CUSTOM_FIELD_LIST),
]
