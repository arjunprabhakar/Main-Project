import calendar
from datetime import datetime, timedelta
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




from django.contrib import admin
from django.db.models import Q
from datetime import datetime

from .models import Product

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Filter Product'
    parameter_name = 'created__range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('this_week', 'This week'),
            ('last_week', 'Last week'),
            ('this_month', 'This month'),
            ('last_month', 'Last month'),
            # ('custom', 'Custom range'),
             ('this_year', 'This year'),
            ('last_year', 'Last year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = datetime.now().date()
            return queryset.filter(created__date=today)
        elif self.value() == 'yesterday':
            yesterday = datetime.now().date() - timedelta(days=1)
            return queryset.filter(created__date=yesterday)
        elif self.value() == 'this_week':
            start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=6)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_week':
            end_date = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)
            start_date = end_date - timedelta(days=6)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'this_month':
            start_date = datetime(datetime.now().year, datetime.now().month, 1).date()
            end_date = start_date + timedelta(days=calendar.monthrange(datetime.now().year, datetime.now().month)[1] - 1)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_month':
            end_date = datetime(datetime.now().year, datetime.now().month, 1).date() - timedelta(days=1)
            start_date = datetime(end_date.year, end_date.month, 1).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'this_year':
            start_date = datetime(datetime.now().year, 1, 1).date()
            end_date = datetime(datetime.now().year, 12, 31).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_year':
            start_date = datetime(datetime.now().year - 1, 1, 1).date()
            end_date = datetime(datetime.now().year - 1, 12, 31).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        return queryset


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=Productgallery
    extra=1


from django.utils.html import format_html
class ProductAdmin(admin.ModelAdmin):
    list_editable=['selling_price','stock']
    prepoluted_fields={'slug':('name',)}
    list_per_page=20
    actions = [export_users]
    exclude = ('percentage',)
    list_display=['image_tag','name','stock','selling_price']
    inlines=[ProductGalleryInline]
    list_filter = (DateRangeFilter,)
    def image_tag(self, obj):
        return format_html('<img src="{}" height="50"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'
    
    # For Calculating Product Percentage   
    def save_model(self, request, obj, form, change):
        percentage =obj.percentage
        percentage=100-((obj.selling_price/obj.original_price)*100)
        obj.percentage=percentage
        super().save_model(request, obj, form, change)
    class Media:
        css = {
            'all': ('/static/custome.css', ),
        }
admin.site.register(Product,ProductAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display=['product','review','rating','date']
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
# ddd
    # def has_delete_permission(self, request, obj=None):
    #     return False
    verbose_name_plural = "Product Reviews"
admin.site.register(tbl_Review,UserAdmin)