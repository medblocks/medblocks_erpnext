__version__ = "0.0.1"
import frappe
from erpnext.stock.doctype.serial_and_batch_bundle import serial_and_batch_bundle 
from frappe.utils import flt
from frappe.query_builder.functions import CombineDatetime, Sum
from frappe.utils import getdate, nowdate
import calendar

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

def ts_expire_month(kwargs):
	from erpnext.stock.utils import get_combine_datetime

	stock_ledger_entry = frappe.qb.DocType("Stock Ledger Entry")
	batch_ledger = frappe.qb.DocType("Serial and Batch Entry")
	batch_table = frappe.qb.DocType("Batch")

	query = (
		frappe.qb.from_(stock_ledger_entry)
		.inner_join(batch_ledger)
		.on(stock_ledger_entry.serial_and_batch_bundle == batch_ledger.parent)
		.inner_join(batch_table)
		.on(batch_ledger.batch_no == batch_table.name)
		.select(
			batch_ledger.batch_no,
			batch_ledger.warehouse,
			Sum(batch_ledger.qty).as_("qty"),
		)
		.where(batch_table.disabled == 0)
		.where(stock_ledger_entry.is_cancelled == 0)
		.groupby(batch_ledger.batch_no, batch_ledger.warehouse)
	)

	# TS Start
	today = getdate(nowdate())
	next_month = today.month + 1 if today.month < 12 else 1
	year = today.year if today.month < 12 else today.year + 1
	first_day_of_next_month = getdate(f"{year}-{next_month:02d}-01")

	if not kwargs.get("for_stock_levels"):
		query = query.where((batch_table.expiry_date >= first_day_of_next_month) | (batch_table.expiry_date.isnull()))
	# End
	
	if kwargs.get("posting_date"):
		if kwargs.get("posting_time") is None:
			kwargs.posting_time = nowtime()

		timestamp_condition = stock_ledger_entry.posting_datetime <= get_combine_datetime(
			kwargs.posting_date, kwargs.posting_time
		)

		query = query.where(timestamp_condition)

	for field in ["warehouse", "item_code"]:
		if not kwargs.get(field):
			continue

		if isinstance(kwargs.get(field), list):
			query = query.where(stock_ledger_entry[field].isin(kwargs.get(field)))
		else:
			query = query.where(stock_ledger_entry[field] == kwargs.get(field))

	if kwargs.get("batch_no"):
		if isinstance(kwargs.batch_no, list):
			query = query.where(batch_ledger.batch_no.isin(kwargs.batch_no))
		else:
			query = query.where(batch_ledger.batch_no == kwargs.batch_no)

	if kwargs.based_on == "LIFO":
		query = query.orderby(batch_table.creation, order=frappe.qb.desc)
	elif kwargs.based_on == "Expiry":
		query = query.orderby(batch_table.expiry_date)
	else:
		query = query.orderby(batch_table.creation)

	if kwargs.get("ignore_voucher_nos"):
		query = query.where(stock_ledger_entry.voucher_no.notin(kwargs.get("ignore_voucher_nos")))

	data = query.run(as_dict=True,debug=1)

	return data

serial_and_batch_bundle.get_available_batches =  ts_expire_month
serial_and_batch_bundle.get_qty_based_available_batches = ts_get_qty_based_available_batches