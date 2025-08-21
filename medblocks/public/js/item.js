
frappe.require("assets/erpnext/js/utils/serial_no_batch_selector.js", function () {
  class CustomSerialBatchPackageSelector extends erpnext.SerialBatchPackageSelector {
    render_data(render = true) {
      if (render) {
        super.render_data();
      }
    }
    
    get_filter_fields() {
      let fields = super.get_filter_fields();
    
      // TS Start
      let based_on_field = fields.find(f => f.fieldname === "based_on");
      if (based_on_field) {
        based_on_field.default = "Expiry";
      }
    
      return fields;
      // End
    }

    get_dialog_table_fields() {
      let fields = super.get_dialog_table_fields();
      let me = this;

      // TS Start
      const batchField = fields.find(f => f.fieldname === "batch_no");
      if (batchField) {
      
        batchField.onchange = function () {
          const doc = this.doc;

          if (!doc.qty && me.item.type_of_transaction === "Outward") {
            me.get_batch_qty(doc.batch_no, (qty) => {
              doc.qty = qty;
              this.grid.set_value("qty", qty, doc);
            });
          }

          me.dialog.fields_dict.entries.df.data.forEach(row => {
              frappe.db.get_value("Batch", row.batch_no, "expiry_date").then(r => {
                if (r.message.expiry_date) {
                    row.expiry_date = r.message.expiry_date
                    me.dialog.refresh()
                }
              });
          });
        };
      }

      const hasExpiryDate = fields.some(f => f.fieldname === "expiry_date");
      if (!hasExpiryDate) {
        fields.push({
          fieldname: "expiry_date",
          fieldtype: "Date",
          label: __("Expiry Date"),
          read_only: 1,
          in_list_view: 1,
        });
      }

      let batch_field = fields.find(f => f.fieldname === "batch_no");
      if (batch_field) {
        batch_field.get_route_options_for_new_doc = () => {
          return {
            item: this.item.item_code,
            item_name: this.item.item_name || this.item.item_code,
          };
        };
      }
    
      return fields;
      // End
    }
    
  }

  // Overwrite the global class
  erpnext.SerialBatchPackageSelector = CustomSerialBatchPackageSelector;
});
  