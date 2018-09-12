frappe.ui.form.on("Supplier Engagement Report Settings", "yellow_zone_start_value", function (frm) {
    cur_frm.set_value("red_zone_end_value", frm.doc.yellow_zone_start_value);
    
    frm.doc.yellow_zone_start_value!=null?(val1=parseFloat(frm.doc.yellow_zone_start_value.toPrecision(2))+0.1):(val1='not set');
    frm.doc.yellow_zone_end_value!=null?(val2=parseFloat(frm.doc.yellow_zone_end_value.toPrecision(2))+0.0):(val2='not set');
    cur_frm.set_value("note", "Color 2 will be shown between "+val1 +" and "+val2);

    
});


frappe.ui.form.on("Supplier Engagement Report Settings", "yellow_zone_end_value", function (frm) {
    cur_frm.set_value("green_zone_start_value", frm.doc.yellow_zone_end_value);
    frm.doc.yellow_zone_start_value!=null?(val1=parseFloat(frm.doc.yellow_zone_start_value.toPrecision(2))+0.1):(val1='not set');
    frm.doc.yellow_zone_end_value!=null?(val2=parseFloat(frm.doc.yellow_zone_end_value.toPrecision(2))+0.0):(val2='not set');
    cur_frm.set_value("note", "Color 2 will be shown between "+val1 +" and "+val2)
});

frappe.ui.form.on("Supplier Engagement Report Settings", "onload", function (frm) {
    cur_frm.set_value("red_zone_end_value", frm.doc.yellow_zone_start_value);
    cur_frm.set_value("green_zone_start_value", frm.doc.yellow_zone_end_value);
    frm.doc.yellow_zone_start_value!=null?(val1=parseFloat(frm.doc.yellow_zone_start_value.toPrecision(2))+0.1):(val1='not set');
    frm.doc.yellow_zone_end_value!=null?(val2=parseFloat(frm.doc.yellow_zone_end_value.toPrecision(2))+0.0):(val2='not set');
    cur_frm.set_value("note", "Color 2 will be shown between "+val1 +" and "+val2)
});