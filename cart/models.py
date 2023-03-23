from email.policy import default
from django.db import models

from credentialapp.models import log_user, user_address
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
    
class Payment(models.Model):
    person = models.ForeignKey(log_user, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    token=models.IntegerField(default=673456)

    def _str_(self):
        return self.customer.fname

class OrderPlaced(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(log_user, on_delete=models.SET_NULL, null=True)
    # customer = models.ForeignKey(user_address,on_delete=models.SET_NULL, null=True,default=1)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_cost(self):
        return self.quantity

    def _str_(self):
        return self.customer.fname
    
    class Meta:
        verbose_name_plural = "Order Details"
        