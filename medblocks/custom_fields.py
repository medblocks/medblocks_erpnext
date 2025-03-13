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
                "insert_after": "medblocks_section_break"
            },
            {
                "fieldname": "from_ignite",
                "label": "From ignite",
                "fieldtype": "Check",
                "depends_on": "eval:doc.fhir_id!=null",
                "read_only": 1,
                "default": "0",
                "insert_after": "fhir_id"
            },
            {
                "fieldname": "mrd_no",
                "label": "UHID No",
                "fieldtype": "Data",
                "in_list_view": 1,
                "allow_in_quick_entry": 1,
                "in_standard_filter": 1,
                "in_global_search": 1,
                "insert_after": "from_ignite"
            },
            {
                "fieldname": "dob",
                "label": "DOB",
                "fieldtype": "Date",
                "insert_after": "mrd_no"
            },  
            {
                "fieldname": "age",
                "label": "Age",
                "fieldtype": "Data",
                "read_only": 1,
                "insert_after": "dob",
            },
            { "fieldname": "medblocks_column_break_1",
                "fieldtype": "Column Break",
                "insert_after": "age",
            },
            {
                "fieldname": "relation_type",
                "label": "Relation Type",
                "fieldtype": "Data",
                "insert_after": "medblocks_column_break_1",
            },
            {
                "fieldname": "relation_name",
                "label": "Relation Name",
                "fieldtype": "Data",
                "insert_after": "relation_type",
            }
]
CONTACT_CUSTOM_FIELD_LIST = [
    medblocks_section_break,
    {
                "fieldname": "mrd_no",
                "label": "UHID No",
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
        "label": "UHID No",
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
        "label": "UHID No",
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
        "label": "UHID No",
        "depends_on": "eval:doc.party_type=='Customer' && doc.party",
        "insert_after": "party_name",
    }
]

OPPORTUNITY_CUSTOM_FIELD_LIST = [
            {
                "fieldname": "mrd_no",
                "label": "UHID No",
                "fieldtype": "Data",
                "depends_on": "eval:doc.opportunity_from=='Customer' && doc.party_name",
        "insert_after": "party_name",
                "in_list_view": 1,
                "in_filter": 1,
                "allow_in_quick_entry": 1,
                "in_standard_filter": 1,
                "in_global_search": 1,
            },
            {**medblocks_section_break, "insert_after": "probability"},
            {
                "fieldname": "screening_purpose",
                "label": "Screening Purpose",
                "fieldtype": "Data",
                "insert_after": "medblocks_section_break",
                "in_list_view": 1,
            },
            {
                "fieldname": "patient_occupation",
                "label": "Patient Occupation",
                "fieldtype": "Data",
                 "insert_after": "screening_purpose",
            },
            {
                "fieldname": "opportunity_source",
                "label": "How did patient know us ?",
                "fieldtype": "Link",
                "options": "Lead Source",
                 "insert_after": "patient_occupation",
            },
            {
                "fieldname": "patient_opinion",
                "label": "Patient Opinion",
                "fieldtype": "Data",
                 "insert_after": "opportunity_source",
            },
            { "fieldname": "medblocks_column_break_1",
                "insert_after": "patient_opinion",
                "fieldtype": "Column Break",
            },
            {
                "fieldname": "payor",
                "label": "Payor",
                "fieldtype": "Select",
                 "insert_after": "medblocks_column_break_1",
                 "options": "\nSelf Pay\nPrivate Insurance\nGovernment insurance",
                 "default": "Self Pay"
            },
            {
                "fieldname": "patient_education",
                "label": "Patient Education",
                "fieldtype": "Data",
                 "insert_after": "payor",
            },
            {
                "fieldname": "surgery_type",
                "label": "Surgery Type",
                "fieldtype": "Link",
                "options": "Item",
                 "in_list_view": 1,
                "in_filter": 1,
                "in_standard_filter": 1,
                 "insert_after": "patient_education",
            },
            {
                "fieldname": "follow_up_date",
                "label": "Follow Up Date",
                "fieldtype": "Date",
                "in_list_view": 1,
                "in_filter": 1,
                "in_standard_filter": 1,
                 "insert_after": "surgery_type",
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
    generate_custom_field_tuple("Opportunity", OPPORTUNITY_CUSTOM_FIELD_LIST),
]
