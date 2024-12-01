import click
import frappe
from medblocks.custom_fields import MEDBLOCKS_CUSTOM_FIELDS
from medblocks.custom_searches import MEDBLOCKS_CUSTOM_SEARCHES


def after_uninstall():
    try:
        for doc_type, custom_fields in MEDBLOCKS_CUSTOM_FIELDS:
            for custom_field in custom_fields:
               delete_custom_field(doc_type, custom_field.get("fieldname"))
            frappe.clear_cache(doctype=doc_type)
        for doc_type, custom_searches in MEDBLOCKS_CUSTOM_SEARCHES:
            delete_custom_search_fields(doc_type, custom_searches)
            frappe.clear_cache(doctype=doc_type)
    except Exception as e:
        click.secho(
            ("Failed removing field Medblocks custom fields"),
            fg="bright_red",
        )
        raise e
    frappe.clear_cache(doctype="Customer")
    click.secho("Medblocks App uninstallation complete", fg="green")


def delete_custom_field(doc_type, field_name):
    custom_field_data = {"dt": doc_type, "fieldname": field_name}
    try:
        existing_custom_field = frappe.db.exists("Custom Field", custom_field_data)
        if existing_custom_field:
            frappe.db.delete(
                "Custom Field",
                custom_field_data,
            )
            frappe.db.commit()
            click.secho(f"Removed custom field `{doc_type}`.`{field_name}`.", fg="white")
        else:
            click.secho(
                (
                    f"Custom field {doc_type}.{field_name} does not exists"
                    "Skipping deletion"
                ),
                fg="yellow",
            )
    except Exception as e:
        click.secho(
            (f"Error deleting Custom Field: {field_name}"),
            fg="bright_red",
        )
        raise e
def delete_custom_search_fields(doc_type,custom_search_data):
    try:
        doc = frappe.get_doc("DocType", doc_type)
        doc.reload()
        search_fields = doc.search_fields.split(",") if doc.search_fields else []
        search_fields = [field.strip() for field in search_fields]

        search_fields = [field for field in search_fields if field not in custom_search_data]
        frappe.db.set_value("DocType",doc_type,"search_fields", ",".join(search_fields))
        frappe.db.commit()
        
        click.secho(f"Removed custom search in `{doc_type}`: {','.join(custom_search_data)}.", fg="white")
    except Exception as e:
        click.secho(
            (f"Error removing custom search in `{doc_type}`: {','.join(custom_search_data)}."),
            fg="bright_red",
        )
        raise e