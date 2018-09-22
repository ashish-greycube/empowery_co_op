frappe.ui.form.on('Supplier', {
    onload: function (doc, dt, dn) {
        if (doc.is_new() != 1) {
            frappe.call({
                method: "empowery_co_op.api.get_linked_customer",
                args: {
                    suppname: cur_frm.doc.supplier_name,
                },
                callback: function (r) {
                    if (!r.message) {
                        const html = `There is no customer linked data for ` + cur_frm.doc.supplier_name
                        $(cur_frm.fields_dict.linked_customer_data.wrapper).html(html);
                    }
                    const linked_customer_data = r.message;
                    if (linked_customer_data) {
                        const html = `
                        <table class="table table-bordered">
                            <thead><tr><th>${__("#")}</th><th>${__("Type")}</th><th>${__("Customer Name")}</th><th>${__("Created Date")}</th></tr></thead>
                            <tbody>
                                ${linked_customer_data.map((c,i) => `<tr><td>${i+1}</td><td>${c.link_doctype}</td><td>${c.link_name}</td>
                                    <td>${c.join_date}</td></tr>`
                                ).join('')}
                            </tbody>
                        </table>`
                        $(cur_frm.fields_dict.linked_customer_data.wrapper).html(html);
                    }
                }
            });
        }
    },
    onload_post_render: function (frm) {
        if(!frm.doc.offer_headline){
            headline_length = 'Allowed Tags:{exp_dt},&lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-0'+ ' Max-50'
            frm.set_df_property('offer_headline', 'description', headline_length);
        }else{
            headline_length = 'Allowed Tags:{exp_dt},&lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-' + frm.doc.offer_headline.length + ' Max-50'
            frm.set_df_property('offer_headline', 'description', headline_length);
        }
        if(!frm.doc.offer_summary){
            summary_length = 'Allowed Tag: &lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-0' + ' Max-42'
            frm.set_df_property('offer_summary', 'description', summary_length);
        }else{
            summary_length = 'Allowed Tag: &lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-' + frm.doc.offer_summary.length + ' Max-42'
            frm.set_df_property('offer_summary', 'description', summary_length);
        }
    },

    offer_headline: function (frm) {
        headline_length = 'Allowed Tags:{exp_dt},&lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-' + frm.doc.offer_headline.length + ' Max-50'
        frm.set_df_property('offer_headline', 'description', headline_length);
    },
    offer_summary: function (frm) {
        summary_length = 'Allowed Tag: &lt;br&gt;' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Current char count-' + frm.doc.offer_summary.length + ' Max-42'
        frm.set_df_property('offer_summary', 'description', summary_length);
    },
    validate: function (frm) {
        if (frm.doc.display_on_partner_listing_page == 1) {
            if (!(frm.doc.service_category) || (frm.doc.geo_location.length == 0)) {
                var msg = "For vendor listing, 'service category' and 'geo location' are mandatory";
                msgprint(msg);
                throw msg;
            }
        }
    }
});