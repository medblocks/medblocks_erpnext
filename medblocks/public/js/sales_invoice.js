// Medblocks
frappe.ui.form.on("Sales Invoice", {
  refresh(frm) {
    if (frm.doc.docstatus === 0 && !frm.doc.is_return) {
      frm.add_custom_button(
        __("Ignite Services"),
        function () {
          get_ignite_services_to_invoice(frm);
        },
        __("Get Items From")
      );
    }
  },

  patient(frm) {
    if (frm.doc.patient) {
      console.log(frm.doc.patient);
      frappe.db.get_value("Patient", frm.doc.patient, "customer").then((r) => {
        if (!r.exc && r.message.customer) {
          frm.set_value("customer", r.message.customer);
        } else {
          frappe.show_alert({
            indicator: "warning",
            message: __("Patient <b>{0}</b> is not linked to a Customer", [
              `<a class='bold' href='/app/patient/${frm.doc.patient}'>${frm.doc.patient}</a>`,
            ]),
          });
          frm.set_value("customer", "");
        }
        frm.set_df_property("customer", "read_only", frm.doc.customer ? 1 : 0);
      });
    } else {
      frm.set_value("customer", "");
      frm.set_df_property("customer", "read_only", 0);
    }
  },

  service_unit: function (frm) {
    set_service_unit(frm);
  },

  items_add: function (frm) {
    set_service_unit(frm);
  },
});

var set_service_unit = function (frm) {
  if (frm.doc.service_unit && frm.doc.items.length > 0) {
    frm.doc.items.forEach((item) => {
      if (!item.service_unit) {
        frappe.model.set_value(
          item.doctype,
          item.name,
          "service_unit",
          frm.doc.service_unit
        );
      }
    });
  }
};

var get_ignite_services_to_invoice = function (frm) {
  var me = this;
  let selected_patient = "";
  let selected_encounter = "";
  var dialog = new frappe.ui.Dialog({
    title: __("Get Items from Ignite Services"),
    fields: [
      {
        fieldtype: "Link",
        options: "Patient",
        label: "Patient",
        fieldname: "patient",
        reqd: true,
      },
      {
        fieldtype: "Link",
        options: "Patient Encounter",
        label: "Patient Encounter",
        fieldname: "encounter",
        reqd: true,
        get_query: function (doc) {
          return {
            filters: {
              patient: dialog.get_value("patient"),
              company: frm.doc.company,
              docstatus: 1,
            },
          };
        },
      },
      { fieldtype: "Section Break" },
      { fieldtype: "HTML", fieldname: "results_area" },
    ],
  });
  var $wrapper;
  var $results;
  var $placeholder;
  dialog.set_values({
    patient: frm.doc.patient,
    encounter: "",
  });
  dialog.fields_dict["encounter"].df.onchange = () => {
    var patient = dialog.fields_dict.patient.input.value;
    var encounter = dialog.fields_dict.encounter.input.value;
    if (encounter && encounter!=selected_encounter) {
      selected_patient = patient;
      selected_encounter = encounter;
      var method = "medblocks.medblocks.utils.get_ignite_services_to_invoice";
      var args = { patient: patient, company: frm.doc.company, encounter: encounter };
      var columns = ["service", "reference_type", "rate"];
      get_ignite_items(
        frm,
        true,
        $results,
        $placeholder,
        method,
        args,
        columns
      );
    } else if (!encounter) {
      selected_encounter = "";
      $results.empty();
      $results.append($placeholder);
    }
  };
  $wrapper = dialog.fields_dict.results_area.$wrapper
    .append(`<div class="results"
		style="border: 1px solid #d1d8dd; border-radius: 3px; height: 300px; overflow: auto;"></div>`);
  $results = $wrapper.find(".results");
  $placeholder = $(`<div class="multiselect-empty-state">
				<span class="text-center" style="margin-top: -40px;">
					<i class="fa fa-2x fa-heartbeat text-extra-muted"></i>
					<p class="text-extra-muted">No billable Ignite Services found</p>
				</span>
			</div>`);
  $results.on("click", ".list-item--head :checkbox", (e) => {
    $results
      .find(".list-item-container .list-row-check")
      .prop("checked", $(e.target).is(":checked"));
  });
  set_primary_action(frm, dialog, $results, true);
  dialog.show();
};

var get_ignite_items = function (
  frm,
  invoice_ignite_services,
  $results,
  $placeholder,
  method,
  args,
  columns
) {
  var me = this;
  $results.empty();
  frappe.call({
    method: method,
    args: args,
    callback: function (data) {
      if (data.message) {
        $results.append(make_list_row(columns, invoice_ignite_services));
        for (let i = 0; i < data.message.length; i++) {
          $results.append(
            make_list_row(columns, invoice_ignite_services, data.message[i])
          );
        }
      } else {
        $results.append($placeholder);
      }
    },
  });
};

var make_list_row = function (columns, invoice_ignite_services, result = {}) {
  var me = this;
  // Make a head row by default (if result not passed)
  let head = Object.keys(result).length === 0;
  let contents = ``;
  columns.forEach(function (column) {
    contents += `<div class="list-item__content ellipsis">
			${
        head
          ? `<span class="ellipsis">${__(frappe.model.unscrub(column))}</span>`
          : column !== "name"
          ? `<span class="ellipsis">${__(result[column])}</span>`
          : `<a class="list-id ellipsis">
						${__(result[column])}</a>`
      }
		</div>`;
  });

  let $row = $(`<div class="list-item">
		<div class="list-item__content" style="flex: 0 0 10px;">
			<input type="checkbox" class="list-row-check" ${
        result.checked ? "checked" : ""
      }>
		</div>
		${contents}
	</div>`);

  $row = list_row_data_items(head, $row, result, invoice_ignite_services);
  return $row;
};

var set_primary_action = function (
  frm,
  dialog,
  $results,
  invoice_ignite_services
) {
  var me = this;
  dialog.set_primary_action(__("Add"), function () {
    frm.clear_table("items");
    let checked_values = get_checked_values($results);
    if (checked_values.length > 0) {
      if (invoice_ignite_services) {
        frm.set_value("patient", dialog.fields_dict.patient.input.value);
      }
      add_to_item_line(frm, checked_values, invoice_ignite_services);
      dialog.hide();
    } else {
      if (invoice_ignite_services) {
        frappe.msgprint(__("Please select Ignite Service"));
      }
    }
  });
};

var get_checked_values = function ($results) {
  return $results
    .find(".list-item-container")
    .map(function () {
      let checked_values = {};
      if ($(this).find(".list-row-check:checkbox:checked").length > 0) {
        checked_values["dn"] = $(this).attr("data-dn");
        checked_values["dt"] = $(this).attr("data-dt");
        checked_values["item"] = $(this).attr("data-item");
        if ($(this).attr("data-rate") != "undefined") {
          checked_values["rate"] = $(this).attr("data-rate");
        } else {
          checked_values["rate"] = false;
        }
        if ($(this).attr("data-income-account") != "undefined") {
          checked_values["income_account"] = $(this).attr(
            "data-income-account"
          );
        } else {
          checked_values["income_account"] = false;
        }
        if ($(this).attr("data-qty") != "undefined") {
          checked_values["qty"] = $(this).attr("data-qty");
        } else {
          checked_values["qty"] = false;
        }
        if ($(this).attr("data-description") != "undefined") {
          checked_values["description"] = $(this).attr("data-description");
        } else {
          checked_values["description"] = false;
        }
        return checked_values;
      }
    })
    .get();
};

var list_row_data_items = function (
  head,
  $row,
  result,
  invoice_ignite_services
) {
  if (invoice_ignite_services) {
    head
      ? $row.addClass("list-item--head")
      : ($row = $(`<div class="list-item-container"
				data-dn= "${result.service}" data-dt= "${result.reference_type}" data-item= "${result.service}"
				data-rate = ${result.rate}
				data-income-account = "${result.income_account}"
				data-qty = ${result.quantity}
				data-description = "${result.description}">
				</div>`).append($row));
  }
  return $row;
};

var add_to_item_line = function (frm, checked_values, invoice_ignite_services) {
  if (invoice_ignite_services) {
    frappe.call({
      doc: frm.doc,
      method: "set_medblocks_services",
      args: {
        checked_values: checked_values,
      },
      callback: function () {
        frm.trigger("validate");
        frm.refresh_fields();
      },
    });
    // for (let i = 0; i < checked_values.length; i++) {
    //   var si_item = frappe.model.add_child(
    //     frm.doc,
    //     "Sales Invoice Item",
    //     "items"
    //   );
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "item_code",
    //     checked_values[i]["item"]
    //   );
    //   frappe.model.set_value(si_item.doctype, si_item.name, "qty", 1);
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "reference_dn",
    //     checked_values[i]["dn"]
    //   );
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "reference_dt",
    //     checked_values[i]["dt"]
    //   );
    // console.log(checked_values[i]["rate"]);
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "rate",
    //     checked_values[i]["rate"]
    //   );
    //   if (checked_values[i]["qty"] > 1) {
    //     frappe.model.set_value(
    //       si_item.doctype,
    //       si_item.name,
    //       "qty",
    //       parseFloat(checked_values[i]["qty"])
    //     );
    //   }
    // }
    // frm.refresh_fields();
  } else {
    // for (let i = 0; i < checked_values.length; i++) {
    //   var si_item = frappe.model.add_child(
    //     frm.doc,
    //     "Sales Invoice Item",
    //     "items"
    //   );
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "item_code",
    //     checked_values[i]["item"]
    //   );
    //   frappe.model.set_value(si_item.doctype, si_item.name, "qty", 1);
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "reference_dn",
    //     checked_values[i]["dn"]
    //   );
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "reference_dt",
    //     checked_values[i]["dt"]
    //   );
    //   frappe.model.set_value(
    //     si_item.doctype,
    //     si_item.name,
    //     "base_rate",
    //     checked_values[i]["rate"]
    //   );
    //   if (checked_values[i]["qty"] > 1) {
    //     frappe.model.set_value(
    //       si_item.doctype,
    //       si_item.name,
    //       "qty",
    //       parseFloat(checked_values[i]["qty"])
    //     );
    //   }
    // }
    // frm.refresh_fields();
  }
};
