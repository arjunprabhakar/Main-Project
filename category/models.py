from django.db import models
from django.db.models.signals import pre_save
from smartstore.utils import unique_slug_generator


#Category Table
class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,null=True,blank=True,editable=False)
    description=models.TextField(blank=True)
    
    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'
     

    def __str__(self):
        return  '{}' .format(self.name)

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Category)


#Subcategory Table
class Subcategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategorys')
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,null=True,blank=True,editable=False)
    description=models.TextField(blank=True)
    
    class Meta:
        ordering=('name',)
        verbose_name='subcategory'
        verbose_name_plural='subcategories'
    def __str__(self):
        return  '{}' .format(self.name)

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Subcategory)


