from django.contrib import admin

# Register your models here.
from django.contrib import admin
import decimal, csv
from django.http import HttpResponse
from django.db.models import F
import csv

# Register your models here.
from credentialapp.models import reg_user,log_user

def export_users(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Phone No'])
    reg_user = queryset.values_list('name', 'phone_no')
    for user in reg_user:
        writer.writerow(user)
    return response
export_users.short_description = 'Download Customer Details'




class UserAdmin(admin.ModelAdmin):
    list_display=['name','lname','phone_no']
    actions = [export_users]
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    verbose_name_plural = "Customer Details"
admin.site.register(reg_user,UserAdmin)
    
admin.site.register(log_user)


