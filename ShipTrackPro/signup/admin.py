from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(ShippingCompany)    
admin.site.register(OilTankerCompany)   
admin.site.register(PortAuthority)  
admin.site.register(CustomAuthority)