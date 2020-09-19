from django.contrib import admin
from .models import Product
from .models import Category
from .models import Customer
from .models import OrderPlaced

# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminOrder(admin.ModelAdmin):
    list_display = ['product', 'customer']


admin.site.register(Customer)
admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(OrderPlaced, AdminOrder)