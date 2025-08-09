from django.contrib import admin
from .models import ProductModel, OrdersModel

# Register your models here.
admin.site.register(ProductModel)
admin.site.register(OrdersModel)