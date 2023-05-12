from django.db import models
from django.core.validators import RegexValidator

from category.models import Category



#Login Table
class log_user(models.Model):
     email= models.EmailField(max_length=200,primary_key=True,unique=True)
     password = models.CharField(max_length=200,default=1 )
     otp = models.IntegerField(default=1)
     type = models.IntegerField(default=0)
     status = models.BooleanField(default=False)
     def __str__(self):
        return self.email
     class Meta:
        verbose_name_plural = "Service Team"

#Customer Registration Table
class reg_user(models.Model):
    email=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    name = models.CharField(max_length=200,verbose_name='First Name')
    lname = models.CharField(max_length=200,verbose_name='Last Name')
    phone_no = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Customer "

    
#Customer Address Table
class user_address(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    fname = models.CharField(max_length=200,verbose_name='First Name')
    lname = models.CharField(max_length=200,verbose_name='Last Name')
    phone_no = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    hname = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    state=models.CharField(max_length=200,null=True)
    pin=models.CharField(max_length=200)


    def __str__(self):
        return self.fname

    # class Meta:
    #     verbose_name_plural = "Customer Details"






#  *********************************  Servicer Module Models **************************************




#Servicer Details Table
class Servicer_Details(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200,verbose_name='First Name',null=True)
    lname = models.CharField(max_length=200,verbose_name='Last Name',null=True)
    phone_no = models.CharField(max_length=200,null=True)
    hname = models.CharField(max_length=200,null=True)
    street = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    district=models.CharField(max_length=200,null=True)
    pin=models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to='Service',blank=True)
    status=models.BooleanField(default=0)
    def __str__(self):
        return self.fname
    class Meta:
        verbose_name_plural = "Service Team Details"


# Customer request for service 
class Servicer_Product(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    category = models.CharField(max_length=200,null=True)
    brand = models.CharField(max_length=200,null=True)
    model = models.CharField(max_length=200,null=True)
    model_no = models.CharField(max_length=200,null=True)
    waranty = models.CharField(max_length=200,null=True)
    issues=models.CharField(max_length=300,null=True)
    bill=models.FileField(upload_to='Bill',blank=True)
    date=models.DateTimeField(auto_now_add=True,null=True)
    status=models.BooleanField(default=0)


# Servicer Accepted Product
class tbl_Accepted_product(models.Model):
    Servicer=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    product=models.ForeignKey(Servicer_Product,on_delete=models.CASCADE)
    status=models.BooleanField(default=0)
    work_done=models.BooleanField(default=0)
    accepted_date=models.DateTimeField(auto_now_add=True,null=True)
    work_hour=models.IntegerField(null=True)
    service_bill=models.FileField(upload_to='Service_Bill',null=True)



# for service bill generation
class tbl_ServiceBill(models.Model):
    Servicer=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    Accepted_product=models.ForeignKey(Servicer_Product,on_delete=models.CASCADE)
    sparepart=models.CharField(max_length=300,null=True)
    amount=models.DecimalField(max_digits=20,decimal_places=2,null=True)
    status=models.BooleanField(default=0)





















# Servicer Accepted Product
class tbl_Accepted_product_status(models.Model):
    Servicer=models.ForeignKey(tbl_Accepted_product,on_delete=models.CASCADE,verbose_name='Email')
    status_head = models.CharField(max_length=200,null=True)
    status_message = models.CharField(max_length=200,null=True)
    date=models.DateTimeField(auto_now_add=True,null=True)
    status = models.BooleanField(default=0)
    











  