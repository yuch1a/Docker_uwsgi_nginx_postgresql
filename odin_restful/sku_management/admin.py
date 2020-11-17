from django.contrib import admin
from .models import *
# Register your models here.

class SKUAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'modified_at')
    list_filter = ('product',)

admin.site.register(SKU, SKUAdmin)
admin.site.register(Product)
admin.site.register(TestConfig)
admin.site.register(ManufacturingOrder)
