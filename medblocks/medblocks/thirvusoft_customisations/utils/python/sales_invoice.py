import frappe 
from datetime import datetime
from erpnext.stock.serial_batch_bundle import SerialBatchCreation


def check_batch_expiry_date(doc,method):
    if not doc.is_return and not doc.is_pos:
        batch_list = []
        expiry_month = []
        expiry_within_days = []
        expiry_date_difference = []

        for item in doc.items:
            if not item.serial_and_batch_bundle:
                sn_doc = SerialBatchCreation(
                    {
                        "item_code": item.item_code,
                        "warehouse": item.warehouse,
                        "voucher_type": doc.doctype,
                        "posting_date": doc.posting_date,
                        "posting_time": doc.posting_time,
                        "qty": item.qty,
                        "type_of_transaction": "Outward" if item.qty > 0 and doc.docstatus < 2 else "Inward",
                        "company": doc.company,
                        "do_not_submit": "True",
                    }
                )

                doc = sn_doc.make_serial_and_batch_bundle()
                item.serial_and_batch_bundle = doc.name



            if item.serial_and_batch_bundle:
                bundle_number = item.serial_and_batch_bundle
                bundle_doc = frappe.get_doc('Serial and Batch Bundle',bundle_number)
                for batch in bundle_doc.entries:
                    batch_number = batch.batch_no 
                    batch_list.append({"batch_no":batch_number,"row_no":item.idx})    


        for check_batch in batch_list:
            batch_document = frappe.get_doc("Batch", check_batch.get("batch_no")) 
            batch_date = (batch_document.expiry_date) 
        
            item_name = batch_document.item_name

            expiry_date_batch = frappe.utils.getdate(batch_date)
            current_date = frappe.utils.getdate(doc.posting_date)

            difference_date = frappe.utils.date_diff(expiry_date_batch,current_date)
        
            current_date_month = current_date.month
            expiry_date_batch_month =  expiry_date_batch.month
        

            target_days = frappe.db.get_single_value('Aarthy Settings',"expiry_days")
            
            if current_date_month == expiry_date_batch_month:
                expiry_month.append((item_name, check_batch.get("batch_no"),check_batch.get("row_no")))

                
            
            elif difference_date <= int(target_days):
                formatted_date = batch_date.strftime("%d-%m-%Y")
                expiry_within_days.append((item_name, check_batch.get("batch_no"),formatted_date, check_batch.get("row_no")))
        

        if len(expiry_month) == 1:
            mes=f"In Row {expiry_month[0][2]}: Item-<b>{expiry_month[0][0]}</b>-Batch:<b>{expiry_month[0][1]}</b> is expired and please select a valid batch.<br>"
            frappe.throw(title = "Restricted Batch",msg = mes) 

        elif len(expiry_month) > 1:
            mes = " "
            for item,batch,row in expiry_month:
                mes += f"In Row {row}: Item:<b>{item}</b>-Batch:<b>{batch}</b> is expired and  Please select a valid batch.<br><br>"
                
            frappe.throw(title = "Restricted Batch",msg = mes) 

                
        
        if len(expiry_within_days) == 1:
            mes = f"In Row {expiry_within_days[0][3]}: Item:  <b>{expiry_within_days[0][0]}</b> with  batch: <b>{expiry_within_days[0][1]}</b> will  expire on <b>{expiry_within_days[0][2]}</b><br><br>"
            frappe.msgprint(title = "Warning",msg = mes)

        elif len(expiry_within_days) > 1:
            mes = " "

            for item, batch, date,row in expiry_within_days:
                mes += f"In Row {row}: Item:  <b>{item}</b> with  batch: <b>{batch}</b> will  expire on <b>{date}</b><br><br>"

            frappe.msgprint(title = "Warning",msg = mes)