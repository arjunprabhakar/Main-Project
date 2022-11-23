from django.contrib import admin


from cart.models import OrderPlaced,Payment

# from cart.models import Payment

# # Register your models here.
# admin.site.register(Payment)


class UserAdmin(admin.ModelAdmin):
    list_display=['user','product']
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = "Order Details"
admin.site.register(OrderPlaced,UserAdmin)