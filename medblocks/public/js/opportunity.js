frappe.ui.form.on("Opportunity", {
party_name: function (frm) {
		if (frm.doc.opportunity_from == "Customer") {
			frappe.call({
            method: "medblocks.medblocks.utils.get_mrd_no",
            args: {
              party: frm.doc.party_name,
            },
            callback: function (response) {
              if (response.message) {
                frm.set_value("mrd_no", response.message.mrd_no);
              }
            },
          });
		}
      else {
         frm.set_value("mrd_no", null);
      }
	},
  source: function (frm) {
  frm.set_value("opportunity_source", frm.doc.source);
	},
  opportunity_source: function (frm) {
  frm.set_value("source", frm.doc.opportunity_source);
	}
  
})