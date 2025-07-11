from django.contrib import admin
from .models import Item, Client, Order, OrderItem

admin.site.register(Item)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(OrderItem)