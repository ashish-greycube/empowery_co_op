// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier Engagement"] = {
  "filters": [

  ],

  "formatter": function (row, cell, value, columnDef, dataContext, default_formatter) {
    value = default_formatter(row, cell, value, columnDef, dataContext);
    if (columnDef.name == '% of Engagement') {
      if (cell == 3) {

        href_start_index = value.search('\">');
        href_end_index = value.search('</a>');
        per_of_engagement = value.slice(href_start_index + 2, href_end_index)

        var $value = $value + $(value).css("background-color", "#75ff3a");
        value = $(value).wrap("<p></p>").parent().html();
        // value = "<span style='background-color:red!important;font-weight:bold'>" + value + "</span>";
      }
    }
    return value;
  }
}