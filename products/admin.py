from django.contrib import admin
from .models import Product,Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

admin.site.site_header = "E-Commerce Control Panel"
admin.site.site_title = "E-Commerce Admin Panel"
admin.site.index_title = "Welcome to the admin panel"
