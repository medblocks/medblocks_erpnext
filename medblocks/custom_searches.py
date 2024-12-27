mrd_number = "mrd_no"

CUSTOMER_CUSTOM_SEARCH_LIST = [mrd_number]
CUSTOMER_CONTACT_SEARCH_LIST = [mrd_number]
SALES_INVOICE_CUSTOM_SEARCH_LIST = [mrd_number]
PAYMENT_ENTRY_CUSTOM_SEARCH_LIST = [mrd_number]
PAYMENT_REQUEST_CUSTOM_SEARCH_LIST = [mrd_number]
OPPORTUNITY_CUSTOM_SEARCH_LIST = [mrd_number]


def generate_custom_search_tuple(dt, custom_list):
    return (dt, custom_list)


MEDBLOCKS_CUSTOM_SEARCHES = [
    generate_custom_search_tuple("Customer", CUSTOMER_CUSTOM_SEARCH_LIST),
    generate_custom_search_tuple("Contact", CUSTOMER_CONTACT_SEARCH_LIST),
    generate_custom_search_tuple("Sales Invoice", SALES_INVOICE_CUSTOM_SEARCH_LIST),
    generate_custom_search_tuple("Payment Entry", PAYMENT_ENTRY_CUSTOM_SEARCH_LIST),
    generate_custom_search_tuple("Payment Request", PAYMENT_REQUEST_CUSTOM_SEARCH_LIST),
    generate_custom_search_tuple("Opportunity", OPPORTUNITY_CUSTOM_SEARCH_LIST),
]
