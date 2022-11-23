

import csv
from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from .models import Product, tbl_Review

def export_users(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Description','Price','Stock','Product Added On'])
    Product = queryset.values_list('name', 'description','price','stock','created')
    for user in Product:
        writer.writerow(user)
    return response
export_users.short_description = 'Download Product Details'

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','stock','available','created','updated']
    list_editable=['price','stock','available']
    prepoluted_fields={'slug':('name',)}
    list_per_page=20
    actions = [export_users]
admin.site.register(Product,ProductAdmin)
# admin.site.register(tbl_Review)

class UserAdmin(admin.ModelAdmin):
    list_display=['product','review','rating','date']
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = "Product Reviews"
admin.site.register(tbl_Review,UserAdmin)