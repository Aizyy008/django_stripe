from django.contrib import admin
from .models import Product, PurchaseHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image')
    search_fields = ('name', 'description')
    list_filter = ('price',)
    ordering = ('id',)
    readonly_fields = ('id',)
    fields = ('id', 'name', 'price', 'description', 'image')
    list_per_page = 20

@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('purchaseID', 'product', 'purchase_done', 'purchase_date')
    search_fields = ('purchaseID', 'product__name')
    list_filter = ('purchase_done', 'purchase_date', 'product')
    ordering = ('-purchase_date',)
    readonly_fields = ('purchase_date',)
    autocomplete_fields = ('product',)
    list_per_page = 25
