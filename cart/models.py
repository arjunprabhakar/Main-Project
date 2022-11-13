from email.policy import default
from django.db import models

from credentialapp.models import log_user
from productapp.models import Product

#Cart Table
class Cart(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    
    def get_product_price(self):
        price=[self.product.price]
        return sum(price)
        
# Wishlist table
class Wishlist(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    