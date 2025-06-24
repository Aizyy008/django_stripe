from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image')
    search_fields = ('name', 'description')
    list_filter = ('price',)
    ordering = ('id',)
    readonly_fields = ('id',)
    fields = ('id', 'name', 'price', 'description', 'image')
    list_per_page = 20
