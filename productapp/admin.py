import admin_thumbnails
import csv
from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from .models import Product, Productgallery, tbl_Review

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


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=Productgallery
    extra=1
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','selling_price','stock','available','created','updated']
    list_editable=['selling_price','stock']
    prepoluted_fields={'slug':('name',)}
    list_per_page=20
    actions = [export_users]
    exclude = ('percentage',)
    list_display=['name','stock','selling_price']
    inlines=[ProductGalleryInline]
    # For Calculating Product Percentage   
    def save_model(self, request, obj, form, change):
        percentage =obj.percentage
        percentage=100-((obj.selling_price/obj.original_price)*100)
        obj.percentage=percentage
        super().save_model(request, obj, form, change)
admin.site.register(Product,ProductAdmin)
# admin.site.register(tbl_Review)


class UserAdmin(admin.ModelAdmin):
    list_display=['product','review','rating','date']
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    verbose_name_plural = "Product Reviews"
admin.site.register(tbl_Review,UserAdmin)