frappe.ui.form.on("Payment Request", "onload", function (frm, dt, dn) {
	if (frm.doc) {
		frappe.call({
			method: "medblocks.medblocks.utils.set_mrd",
			args: { doc: frm.doc },
         callback: function (response) {
         }
		});
	}
});