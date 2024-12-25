from django.contrib import admin
from .models import Order,ExcelSheet


# code to show id of order
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Order,OrderAdmin)
admin.site.register(ExcelSheet)
