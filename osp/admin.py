from django.contrib import admin
from osp.models import Item, Customer

# Register your models here.
admin.site.register(Customer)

class ItemAdmin(admin.ModelAdmin):
    list_filter = ('listed',)
    exclude = ('listed', 'basket', 'wishlist', 'purchase_quantity',)

admin.site.register(Item, ItemAdmin)

