// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
var color_codes = {}
frappe.query_reports["Supplier Engagement"] = {

  "filters": [
  ],
  onload: (report) => {
    frappe.call({
      method: "empowery_co_op.co_op.report.supplier_engagement.supplier_engagement.get_color_codes",
      args: {},
      callback: function (data) {
        color_codes = data.message
      }
    })

  },
  "formatter": function(value, row, column, data, default_formatter) {
  // "formatter": function (row, cell, value, columnDef, dataContext,column,data, default_formatter) {
    value = default_formatter(value, row, column, data);

    if (column.name == '% of Engagement') {
      if (1==1) {
        
        per_of_engagement = null
        href_start_index = value.search('\">');
        href_end_index = value.search('</a>');
        per_of_engagement = parseFloat(value.slice(href_start_index + 2, href_end_index))
        console.log(per_of_engagement)
        if (per_of_engagement != null || per_of_engagement != '') {

          if ((per_of_engagement >= 0.0) && (per_of_engagement <= parseFloat(color_codes.yellow_start))) {
            value = `<p style='margin:0px;padding-left:5px;background-color:${color_codes.color_1}!important;'>${value}</p>`
          } else if (per_of_engagement > parseFloat(color_codes.yellow_start) && per_of_engagement <= parseFloat(color_codes.yellow_end)) {
            value = `<p style='margin:0px;padding-left:5px;background-color:${color_codes.color_2}!important;'>${value}</p>`
          } else if (per_of_engagement > parseFloat(color_codes.yellow_end) && per_of_engagement <= 100.00) {
            value = `<p style='margin:0px;padding-left:5px;background-color:${color_codes.color_3}!important;'>${value}</p>`
          }
          return value;
        }
        return value;
      }
    }
    return value;
  }
}