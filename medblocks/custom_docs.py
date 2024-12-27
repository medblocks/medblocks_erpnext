OPPORTUNITY_TYPE_CUSTOM_FIELD_LIST = [
   {
      "name" : "Surgery"
   }
]
def generate_custom_doc_tuple(dt, custom_list):
    return (dt, list(map(lambda x, doctype=dt: {**x, "doctype": doctype}, custom_list)))

MEDBLOCKS_CUSTOM_DOCS = [
    generate_custom_doc_tuple("Opportunity Type", OPPORTUNITY_TYPE_CUSTOM_FIELD_LIST),
]