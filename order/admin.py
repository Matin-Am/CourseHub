from django.contrib import admin
from .models import Order , OrderItem
# Register your models here.


class OrderItemAmin(admin.TabularInline):
    model = OrderItem



class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAmin,)
    raw_id_fields = ("user",)
    list_display = ("user","total_price","paid")
    list_filter = ("created",)
    search_fields = ("id",)

admin.site.register(Order , OrderAdmin)