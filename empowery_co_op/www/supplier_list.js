

$(document).ready(function() {

    if (frappe.session.user!='Guest') {
        $('[name="sender_name"]').val($('.full-name').text());
    }

   

     // filter vendor list as per dropdown selection
     $('#service_category_selector').change(function() {

        var location=$('#location_category_selector').val()
        var category=$(this).val()

        console.log(location)
        console.log(category)

        if (category=='all_category' && location=='all_location') {
            $('.all_location').show();
        }

        if (location!='all_location' && category=='all_category' ) {
            $('.all_location').hide();
            $('.'+location).show();
        }

        if( (location!='all_location' && category!='all_category') || (location=='all_location' && category!='all_category' )) {
            $('.all_location').hide();
            $("#"+category).filter("."+location).show();
        }

      
    });

          // filter vendor list as per dropdown selection
          $('#location_category_selector').change(function() {
        
            var category=$('#service_category_selector').val()
            var location=$(this).val()

            console.log(location)
            console.log(category)

            if (category=='all_category' && location=='all_location') {
                $('.all_location').show();
            }
    
            if (location!='all_location' && category=='all_category' ) {
                $('.all_location').hide();
                $('.'+location).show();
            }
            if( (location!='all_location' && category!='all_category') || (location=='all_location' && category!='all_category' )) {
                $('.all_location').hide();
                $("#"+category).filter("."+location).show();
            }
          
        });

    // button for sign-up event
  
    $('.btn-request').click(function() {
      // hide any message
      $("#form-alert").toggle(false);

        //selected vendor
        var sel = $('input[type=checkbox]:checked').map(function(_, el) {
            return $(el).val();
        }).get();
    
        if(sel.length == 0) {
            msgprint('Please select supplier for inquiry');
            return;
        }  
  
      var args = {
          sender_name: $('[name="sender_name"]').val(),
          company_name: $('[name="company_name"]').val(),
          email: $('[name="email"]').val(),
          phone: $('[name="phone"]').val()
        }
  
      // all mandatory
      if(!(args.sender_name && args.company_name && args.email
          && args.phone)) {
         msgprint("All fields are necessary. Please try again.");
         return;
      }
  
      // email is valid
      if(!valid_email(args.email)) {
          msgprint('Please enter a valid email id');
          return;
      }



    // check if member or guest
    var is_guest = false
    if (getCookie("full_name")=="Guest"){
        is_guest = true
    }
      // compose the message
      var message = "Company: " + args.company_name + "\n"
          + "Name: " + args.sender_name + "\n"
          + "Email: " + args.email + "\n"
          + "Phone: " + args.phone + "\n" 
          + "Is Guest? : " + is_guest + "\n"


    frappe.call({
            method:'empowery_co_op.www.supplier_list.send_email',
            args:{
                name:args.sender_name,
                company:args.company_name,
                email:args.email,
                phone:args.phone,
                is_guest: is_guest,
                vendor_list:sel
            },
            callback: function(r) {
                          if(r.message) {
                              data=r.message
 
                          }}});
 
    var message = message + "Inquiry for vendor: "+sel
      erpnext.send_message({
        subject:'Inquiry for vendor :'+sel,
        sender: $('[name="email"]').val(),
        status: 'Open',
        message: message,
        callback: function(r) {
              // print return message
          msgprint(r.message);
  
              // clear all inputs
          $(':input').val('');
        }
      });
    });
  
  });
  
  var msgprint = function(txt) {
      $("#form-alert").html(txt).toggle(true);
  }
