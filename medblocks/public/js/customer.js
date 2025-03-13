frappe.ui.form.on("Customer", {
   dob: function (frm) {
            frappe.call({
               method: "medblocks.medblocks.utils.get_age",
               args: {
                 dob: frm.doc.dob,
               },
               callback: function (response) {
                 if (response.message) {
                   frm.set_value("age", response.message.age);
                 }
               },
             });
      }
   })