from django.db import models
from django.db.models.signals import pre_save
from credentialapp.models import log_user
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
    original_price=models.DecimalField(max_digits=20,decimal_places=2,null=True)
    selling_price=models.DecimalField(max_digits=20,decimal_places=2,null=True)
    optimized_price=models.DecimalField(max_digits=20,decimal_places=2,null=True)
    image=models.ImageField(upload_to='product',blank=True)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    percentage=models.IntegerField(default=1)
    sentiment_score=models.FloatField(default=0)
    rate=models.FloatField(default=0.0)

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




class Productgallery(models.Model):
    product=models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='store/products', max_length=255)

    def str(self):
        return self.product.product_name

    class Meta:
        verbose_name='Product Gallery'
        verbose_name_plural='Product gallery'


class tbl_Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,editable=False)
    user=models.ForeignKey(log_user, on_delete=models.CASCADE,editable=False)
    review=models.TextField(max_length=800,blank=True)
    positive_score = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    negative_score = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    neutral_score = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    rating=models.FloatField()
    rate=models.FloatField(default=0.0)
    date=models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
            verbose_name_plural = "Reviews"




class Sentiment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num_reviews = models.IntegerField()
    avg_score = models.FloatField(default=0)
    avg_pos_score = models.FloatField(default=0)
    avg_neg_score = models.FloatField(default=0)
    avg_neu_score = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Sentiments'

    def __str__(self):
        return f'Sentiment for {self.product.name}'
