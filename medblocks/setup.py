# isort: skip_file
import frappe
from erpnext.setup.utils import insert_record
from frappe import _


def setup_Medblocks():
	if frappe.db.exists("Item Group", "Medblocks"):
		# already setup
		return

	medblocks = frappe.new_doc("Item Group")
	medblocks.item_group_name = "Medblocks"
	medblocks.parent_item_group = "All Item Groups"
	medblocks.is_group = 0
	medblocks.insert()

	frappe.clear_cache()