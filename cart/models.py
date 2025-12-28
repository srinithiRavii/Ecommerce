from django.db import models
from store.models import Products


class Cart(models.Model):
    cart_id=models.CharField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
class Cart_item(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_available=models.BooleanField(default=True)
    @property
    def subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return str(self.product)

    

