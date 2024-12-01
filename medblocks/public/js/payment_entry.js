frappe.ui.form.on('Payment Entry', {
   party: function(frm) {
       if (frm.doc.party) {
           frappe.call({
               method: "medblocks.medblocks.utils.get_mrd_no",
               args: {
                   party: frm.doc.party
               },
               callback: function (response) {
                   if (response.message) {
                       frm.set_value("mrd_no", response.message.mrd_no);
                   }
               }
           });
       }
   },
   onload: function(frm) {
       if (frm.doc.party) {
           frappe.call({
               method: "medblocks.medblocks.utils.get_mrd_no",
               args: {
                   party: frm.doc.party
               },
               callback: function (response) {
                   if (response.message) {
                       frm.set_value("mrd_no", response.message.mrd_no);
                   }
               }
           });
       }
   }
});