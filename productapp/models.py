from django.db import models
from django.db.models.signals import pre_save
from smartstore.utils import unique_slug_generator
from category.models import Category,Subcategory
from smart_selects.db_fields import GroupedForeignKey
# Create your models here.

#Product Table
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='ctgry')
    subcategory=GroupedForeignKey(Subcategory,"category",on_delete=models.CASCADE,related_name='sbctgry')
    name=models.CharField(max_length=251,unique=True)
    slug=models.SlugField(max_length=250,unique=True,editable=False)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=20,decimal_places=2)
    image=models.ImageField(upload_to='product',blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('name',)
        verbose_name='product'
        verbose_name_plural='products'

    def __str__(self):
        return  '{}' .format(self.name)
def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Product)
