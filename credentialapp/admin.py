from django.conf import settings
from django.contrib import admin
from django.contrib import admin
import decimal, csv
from django.http import HttpResponse
from django.db.models import F
import csv
from django.core.mail import send_mail
from credentialapp.models import Servicer_Details, Servicer_Product, reg_user,log_user, tbl_Accepted_product, tbl_Accepted_product_status, tbl_ServiceBill, user_address
from hashlib import sha256
from django.template.loader import render_to_string
import re


class ServiceAdmin(admin.ModelAdmin):
    verbose_name_plural = "Add Servicer"
    exclude = ('otp','type','status',)
    list_display=['email']
     
    def save_model(self, request, obj, form, change):
        password1 =obj.password
        password = sha256(obj.password.encode()).hexdigest()
        obj.password=password
        obj.type=1
        obj.status=1
        super().save_model(request, obj, form, change)
        # send Mail
        subject="SmartStore"
        from_email=settings.EMAIL_HOST_USER
        recepient_list = [obj.email]
        htmlgen = 'Welcome to SmartStore...! \n Your Login Credential Is \n Email:'+obj.email+'\n Password:'+password1+'\nLogin Here : http://127.0.0.1:8000/login/'
        send_mail(subject,htmlgen,from_email,recepient_list)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     qs = qs.filter(type=1)
    #     return qs
    
admin.site.register(log_user,ServiceAdmin)
# admin.site.register(Servicer_Product)



# def export_users(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="Users.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Name','Phone No'])
#     reg_user = queryset.values_list('name', 'phone_no')
#     for user in reg_user:
#         writer.writerow(user)
#     return response
# export_users.short_description = 'Download Customer Details'




class UserAdmin(admin.ModelAdmin):
    list_display=['name','phone_no']
    # actions = [export_users]
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    verbose_name_plural = "Customer Details"
admin.site.register(reg_user,UserAdmin)
    

class UserAdmin(admin.ModelAdmin):
    list_display=['fname']
    # actions = [export_users]
    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    # verbose_name_plural = "Customer Details"
admin.site.register(Servicer_Details,UserAdmin)
admin.site.register(tbl_Accepted_product)
admin.site.register(Servicer_Product)
admin.site.register(tbl_ServiceBill)
# admin.site.register(tbl_Accepted_product_status)


    




