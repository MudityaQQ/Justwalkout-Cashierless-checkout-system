from django.contrib import admin
from store.models import *
# Register Product models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=(
        'idProduct',
        'name',
        'price',
        'description',
        'image'
    )


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','customer','quantity','price','date','status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category , AdminCategory)
admin.site.register(Order,OrderAdmin)
