frappe.ui.form.on('Supplier', {
    onload: function (doc, dt, dn) {
        if (doc.is_new() == 0) {
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
                    console.log(r.message)
                    console.log(linked_customer_data)
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
    refresh: function (frm) {
        summary_length = 'Tag:< br>' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Cur length-' + frm.doc.offer_summary.length + ' Max-42'
        frm.set_df_property('offer_summary', 'description', summary_length);

        headline_length = 'Tags:{exp_dt},< br>' + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Cur length-' + frm.doc.offer_headline.length + ' Max-50'
        frm.set_df_property('offer_headline', 'description', headline_length);

    }
});