from django.contrib import admin

# Register your models here.
from .models import Product
from .models import productbuy
admin.site.register(Product)
admin.site.register(productbuy)