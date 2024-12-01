import click
import frappe
from medblocks.custom_fields import MEDBLOCKS_CUSTOM_FIELDS
from medblocks.custom_searches import MEDBLOCKS_CUSTOM_SEARCHES

def before_install():
    try:
        for doc_type, custom_fields in MEDBLOCKS_CUSTOM_FIELDS:
            for custom_field in custom_fields:
                insert_custom_field(custom_field)
                
            frappe.clear_cache(doctype=doc_type)
        for doc_type, custom_searches in MEDBLOCKS_CUSTOM_SEARCHES:
            add_custom_search_fields(doc_type, custom_searches)
            frappe.clear_cache(doctype=doc_type)
    except Exception as e:
        click.secho(
            (
                "Installation for Medblocks failed due to an error.\n"
                "Please try re-installing the app."
            ),
            fg="bright_red",
        )
        raise e
    click.secho("Medblocks App installation complete", fg="green")

def add_custom_search_fields(doc_type,custom_search_data):
    try:
        doc = frappe.get_doc("DocType", doc_type)
        doc.reload()
        search_fields = doc.search_fields.split(",") if doc.search_fields else []
        search_fields = [field.strip() for field in search_fields]
        for field in custom_search_data:
            if field not in search_fields:
                search_fields.append(field)
        frappe.db.set_value("DocType",doc_type,"search_fields", ",".join(search_fields))
        frappe.db.commit()
        
        click.secho(f"Added custom search in `{doc_type}`: {','.join(custom_search_data)}.", fg="white")
    except Exception as e:
        click.secho(
            (f"Error adding Custom search in `{doc_type}`: {','.join(custom_search_data)}."),
            fg="bright_red",
        )
        raise e
def insert_custom_field(custom_field_data):
    try:
        existing_custom_field = frappe.db.exists(
            "Custom Field",
            {
                "dt": custom_field_data.get("dt"),
                "fieldname": custom_field_data.get("fieldname"),
            },
        )
        if not existing_custom_field:
            customer_doc = frappe.new_doc("Custom Field")
            customer_doc.update(custom_field_data)
            customer_doc.insert()
            frappe.db.commit()
            click.secho(f"Added custom field `{custom_field_data.get('dt')}`.`{custom_field_data.get('fieldname')}`.", fg="white")
        else:
            click.secho(
                (
                    f"Custom field `{custom_field_data.get('dt')}`.`{custom_field_data.get('fieldname')}` exists. "
                    "Skipping creation."
                ),
                fg="yellow",
            )
    except Exception as e:
        click.secho(
            (f"Error inserting Custom Field: `{custom_field_data.get('dt')}`.`{custom_field_data.get('fieldname')}`."),
            fg="bright_red",
        )
        raise e
