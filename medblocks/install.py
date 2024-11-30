import click
import frappe


def after_install():
    try:
        custom_fhir_field = frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Customer",
                "fieldname": "fhir_id",
                "fieldtype": "Data",
                "hidden": 1,
                "name": "fhir_id",
                "label": "Fhir Id",
            }
        )
        custom_fhir_field.insert(ignore_permissions=True)
        custom_fhir_field.submit()
        custom_uid_field = frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Customer",
                "fieldname": "customer_uid",
                "fieldtype": "Data",
                "hidden": 0,
                "name": "customer_uid",
                "label": "Customer Uid",
            }
        )
        custom_uid_field.insert(ignore_permissions=True)
        custom_uid_field.submit()
        frappe.clear_cache(doctype="Customer")
    except Exception as e:
        click.secho(
            (
                "Installation for Medblocks failed due to an error."
                " Please try re-installing the app or"
            ),
            fg="bright_red",
        )
        raise e
    click.secho("Medblocks App installation complete", fg="green")
