__version__ = "0.0.1"
import frappe
from erpnext.stock.doctype.serial_and_batch_bundle import serial_and_batch_bundle 
from frappe.utils import flt

def ts_get_qty_based_available_batches(available_batches, qty):
	batches = []
	for batch in available_batches:
		if qty <= 0:
			break

		batch_qty = flt(batch.qty)
		if qty > batch_qty:
			batches.append(
				frappe._dict(
					{
						"batch_no": batch.batch_no,
						"qty": batch_qty,
						"warehouse": batch.warehouse,
						"expiry_date":frappe.get_value('Batch',batch.batch_no,'expiry_date'), #TS Customisation
					}
				)
			)
			qty -= batch_qty
		else:
			batches.append(
				frappe._dict(
					{
						"batch_no": batch.batch_no,
						"qty": qty,
						"warehouse": batch.warehouse,
						"expiry_date":frappe.get_value('Batch',batch.batch_no,'expiry_date'), #TS Customisation
					}
				)
			)
			qty = 0

	return batches

serial_and_batch_bundle.get_qty_based_available_batches = ts_get_qty_based_available_batches