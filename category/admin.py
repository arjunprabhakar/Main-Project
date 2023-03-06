from asyncio import format_helpers
from django.contrib import admin
from django.urls import reverse

from productapp.models import Product


# Register your models here.
from .models import Category,Subcategory
# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['name']
#     prepoluted_fields={'slug':('name',)}
# admin.site.register(Category,CategoryAdmin)





class SubcategoryAdmin(admin.ModelAdmin):
    list_display=['name','category']
    prepoluted_fields={'slug':('name',)}
admin.site.register(Subcategory,SubcategoryAdmin)




