$(document).ready(function () {
    //clear everything
    $('input:checkbox').removeAttr('checked');
    $('.supplier').show()
    $("#form-alert").toggle(false);

    if (frappe.session.user != 'Guest') {
        $('[name="sender_name"]').val($('.full-name').text());
    }

    // on dropdown change
    $('select').change(function () {
        $('input:checkbox').removeAttr('checked');
        var location = '[' + $('#location_category_selector').val() + ']'
        var category = '[' + $('#service_category_selector').val() + ']'
        //hide all first
        $('.supplier').hide()
        //show the matching ones
        $('.supplier[data-category*="' + category + '"][data-location*="' + location + '"]').show()

    });

    // button for sign-up event

    $('.btn-request').click(function () {
        // hide any message
        $("#form-alert").toggle(false);

		$('[name="sender_name"]').removeClass('red');
			$('[name="company_name"]').removeClass('red');
			$('[name="email"]').removeClass('red');
			$('[name="phone"]').removeClass('red');
			
        //selected vendor
        var sel = $('input[type=checkbox]:checked').map(function (_, el) {
            return $(el).val();
        }).get();

        if (sel.length == 0) {
            msgprint('Please select atleast one supplier for inquiry');
            $("#requestButton").focus();
            return;
        }

        var args = {
            sender_name: $('[name="sender_name"]').val(),
            company_name: $('[name="company_name"]').val(),
            email: $('[name="email"]').val(),
            phone: $('[name="phone"]').val()
        }

        // all mandatory
        if (!(args.sender_name && args.company_name && args.email &&
                args.phone)) {
            msgprint("All fields are necessary. Please try again.");
			$('[name="sender_name"]').addClass('red');
			$('[name="company_name"]').addClass('red');
			$('[name="email"]').addClass('red');
			$('[name="phone"]').addClass('red');
			$("#form-alert").attr('class', '');
            $("#form-alert").addClass('alert');
            $("#requestButton").focus();
            return;
        }

        // email is valid
        if (!valid_email(args.email)) {
            msgprint('Please enter a valid email id');
			$('[name="email"]').addClass('red');
			$("#form-alert").attr('class', '');
            $("#form-alert").addClass('alert');
            $("input[name='email']").focus();
            return;
        }



        // check if member or guest
        var is_guest = false
        if (getCookie("full_name") == "Guest") {
            is_guest = true
        }
        // compose the message
        var message = "Company: " + args.company_name + "\n" +
            "Name: " + args.sender_name + "\n" +
            "Email: " + args.email + "\n" +
            "Phone: " + args.phone + "\n" +
            "Is Guest? : " + is_guest + "\n"

        var message = message + "Inquiry for vendor: " + sel
        erpnext.send_message({
            subject: 'Inquiry for vendor :' + sel,
            sender: $('[name="email"]').val(),
            status: 'Open',
            message: message,
            callback: function (r) {
                // print return message
                $("#form-alert").toggle(false);
                if(r.message=='okay')
                msgprint('Your inquiry is submited successfully. Thanks!');
				$("#form-alert").attr('class', '');
                $("#form-alert").addClass('success');
               
				
                $(':input').val('');
                $('input:checkbox').removeAttr('checked');
                $('.supplier').show()
                $("input[name='email']").focus();
                $("#requestButton").focus();

            }
        });

        frappe.call({
            method: 'empowery_co_op.www.vendor_offer_list.send_email',
            args: {
                name: args.sender_name,
                company: args.company_name,
                email: args.email,
                phone: args.phone,
                is_guest: is_guest,
                vendor_list: sel
            },
            callback: function (r) {
                if (r.message) {
                    data = r.message
                    // $("#form-alert").toggle(false);
                    // msgprint('Email sent to ' + data + ' vendor. You will soon hear from them.');
                    $(':input').val('');
                    $('input:checkbox').removeAttr('checked');
                    $('.supplier').show()
                }
            }
        });


    });

});

var msgprint = function (txt) {
    $("#form-alert").html(txt).toggle(true);
}