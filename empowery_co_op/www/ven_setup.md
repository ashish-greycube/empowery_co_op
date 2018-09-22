-----------------------------------------
Steps to do on live

(1)create service category
	3PL & Warehousing
	Accounting / Bookkeeping
	Accounting / Systems
	Business Brokers
	Digital Marketing
	Digital Marketing / Keyword Management
	Digital Marketing / SEO & PPC
	Freelance Design
	IT Products & Services
	Payment Processing
	Photography
	Quality Control/Inspection
	Shipping

(2)create supplier types - 
	Standard Partner
	Affiliate Partner (rename existing Affiliate)
	Supplier Partner

(3)create geo locations -
	USA Only
	Canada Only
	
(3) setup permission for display - Perm code is 1

(4) setup email alert to Empowery Support Team to update information. near expiration date
Supplier Doctype
7 days before offer_expiration_date

sub : {{ doc.name }} :  Offer is about to Expire on {{doc.offer_expiration_date }}
condition : doc.display_on_partner_listing_page == 1

Hi,
<br>
<p>The Offer from Vendor : {{ doc.name}} is about to expire on {{ doc.offer_expiration_date }}
<ul>
<li> Vendor Contact for Offer : {{doc.contact_email_for_offers}} </li>
<il>Offer Headline : {{ doc.offer_headline }} </il>
<il>Offer Expiry Date : {{doc.offer_expiration_date}}</il>
<il>Offer Summary : {{ doc.offer_summary}} </il>
<il>Offer Details : {{doc.more_details}} </il>

</ul>
<br>
Please take necessary action.
 <br>
<br>
Thanks <br>
Team Empowery
</p>

(5) Setup Carousel and Email template

sub: For {vendor_name} : Empowery Lead  from -  {sender_name}

<div>Hi {vendor_name},</div>
<div><br></div>
<div>This is to inform you that following lead is generated on empowery website.&nbsp;</div>
<div>Details as below :</div>
<ol>
<li>Sender Name : {sender_name}</li>
<li>Sender Company: {sender_company}</li>
<li>Sender Email : {sender_email}</li>
<li>Sender Phone : {sender_phone}</li>
<li>Is inquiry coming from an empowery member : {sender_is_guest}</li>
</ol>
<div><br></div>
<div>Thanks,</div>
<div>Team Empowery</div>
