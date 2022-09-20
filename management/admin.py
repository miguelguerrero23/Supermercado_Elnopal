from django.contrib import admin
from management.models import *
from personal.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Buy)
admin.site.register(DetailBuy)
admin.site.register(Sale)
admin.site.register(DetailSale)
admin.site.register(Provider)
