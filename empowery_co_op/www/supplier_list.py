from __future__ import unicode_literals

import frappe
from frappe.utils import now
from frappe import _

def get_context(context):
    slideshow_name='Top 5 Supplier'
    context.slideshow=frappe.db.sql("""select slideshow_name 
from `tabWebsite Slideshow` where name = %s""",slideshow_name,as_dict=1)