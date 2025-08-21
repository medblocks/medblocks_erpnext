import  frappe
import re
from frappe.model.naming import make_autoname
from erpnext.stock.doctype.item.item import Item

def item_auto_series(doc, event):
	abbr = frappe.db.get_value("Item Group", doc.item_group, "custom_abbrevation")
	# if not abbr:
	# 	frappe.throw("Abbreviation not set for this Item Group.")

	last_code = frappe.db.get_value(
		"Item",
		filters={"item_code": ["like", f"{abbr}-%"]},
		fieldname="item_code",
		order_by="item_code DESC"
	)

	last_num = int(re.search(r"(\d+)$", last_code).group(1)) + 1 if last_code else 1
	new_code = f"{abbr}-{last_num:03d}"

	doc.item_code = new_code

class TSItem(Item):
	def validate(self):
		#Start
		# if not self.item_name:
		# 	self.item_name = self.item_code
		#End

		# if not strip_html(cstr(self.description)).strip():
		# 	self.description = self.item_name

		self.validate_uom()
		self.validate_description()
		self.add_default_uom_in_conversion_factor_table()
		self.validate_conversion_factor()
		self.validate_item_type()
		self.validate_naming_series()
		self.check_for_active_boms()
		self.fill_customer_code()
		self.check_item_tax()
		self.validate_barcode()
		self.validate_warehouse_for_reorder()
		self.update_bom_item_desc()

		self.validate_has_variants()
		self.validate_attributes_in_variants()
		self.validate_stock_exists_for_template_item()
		self.validate_attributes()
		self.validate_variant_attributes()
		self.validate_variant_based_on_change()
		self.validate_fixed_asset()
		self.clear_retain_sample()
		self.validate_retain_sample()
		self.validate_uom_conversion_factor()
		self.validate_customer_provided_part()
		self.update_defaults_from_item_group()
		self.validate_item_defaults()
		self.validate_auto_reorder_enabled_in_stock_settings()
		self.cant_change()
		self.validate_item_tax_net_rate_range()

		if not self.is_new():
			self.old_item_group = frappe.db.get_value(self.doctype, self.name, "item_group")


def  validate_abbrivation(doc,method):
	if doc.custom_abbrevation:
		check_abbrivation = doc.custom_abbrevation
		if(check_abbrivation != check_abbrivation.upper()):
			doc.custom_abbrevation = doc.custom_abbrevation.upper()
