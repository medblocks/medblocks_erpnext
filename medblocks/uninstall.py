import click
import frappe
def after_uninstall():
   try:
      frappe.db.delete(
        "Custom Field",
        {
            "fieldname": "fhir_id",
            "dt": "Customer",
        },
      )
   except Exception as e:
      click.secho(
         (
               "Failed removing field fhir_id from Customer"
         ),
         fg="bright_red",
      )
      raise e