frappe.listview_settings['Opportunity'] = {
   formatters: {
      follow_up_date(val,_,doc){
         if(!val) return ""
         if (doc.status !== "Open" && doc.status !=="Quotation")  return `<div class='indicator-pill grey'>${val}</div>`
         const currentDate = frappe.datetime.now_date();
         if ( currentDate >= val) 
         return `<div class='indicator-pill red'>${moment(val).fromNow()}</div>`
         if ( currentDate == val) return `<div class='indicator-pill blue'>${moment(val).fromNow()}</div>`
         else return  `<div class='indicator-pill green'>${moment(val).fromNow()}</div>`
      }
  },
};