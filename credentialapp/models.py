from django.db import models
from django.core.validators import RegexValidator



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
        verbose_name_plural = "Service"

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
    pin=models.CharField(max_length=200)


    def __str__(self):
        return self.fname

    # class Meta:
    #     verbose_name_plural = "Customer Details"




#Customer Address Table
class Servicer_Details(models.Model):
    user=models.ForeignKey(log_user,on_delete=models.CASCADE,verbose_name='Email')
    fname = models.CharField(max_length=200,verbose_name='First Name',null=True)
    lname = models.CharField(max_length=200,verbose_name='Last Name',null=True)
    phone_no = models.CharField(max_length=200,null=True)
    hname = models.CharField(max_length=200,null=True)
    street = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    district=models.CharField(max_length=200,null=True)
    pin=models.CharField(max_length=200,null=True)
    image=models.ImageField(upload_to='Service',blank=True)
    def __str__(self):
        return self.fname


# Service Modules
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



  