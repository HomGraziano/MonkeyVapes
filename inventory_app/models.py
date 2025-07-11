from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name="Producto:")
    quantity = models.IntegerField(default=0,verbose_name="Precio Unitario:")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Cantidad:")

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class Client(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()