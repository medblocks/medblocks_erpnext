(() => {
  // ../medblocks/medblocks/public/js/kanban.js
  frappe.views.KanbanView = class KanbanView extends frappe.views.KanbanView {
    before_render() {
      if (this.doctype == "Opportunity") {
        const data = this.data;
        const mod_data = data == null ? void 0 : data.map((item) => {
          let follow_up_date = item == null ? void 0 : item.follow_up_date;
          if (!follow_up_date)
            return item;
          if ((item == null ? void 0 : item.status) !== "Open" && (item == null ? void 0 : item.status) !== "Quotation") {
            return item;
          }
          let user_tags = item._user_tags;
          const currentDate = frappe.datetime.now_date();
          const currentDateObj = new Date(currentDate);
          const followUpDateObj = new Date(follow_up_date);
          const timeDifference = followUpDateObj - currentDateObj;
          user_tags = user_tags ? user_tags : ",";
          if (currentDate >= follow_up_date)
            user_tags = ",Follow up: Due" + user_tags || "";
          else if (timeDifference > 0 && timeDifference <= 24 * 60 * 60 * 1e3)
            user_tags = ",Follow up: Today" + user_tags || "";
          item._user_tags = user_tags;
          return item;
        });
        this.data = mod_data;
      }
    }
  };
})();
//# sourceMappingURL=medblocks.bundle.XG6VMZBD.js.map
