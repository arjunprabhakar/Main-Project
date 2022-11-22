from django.contrib import admin


from cart.models import OrderPlaced,Payment

# from cart.models import Payment

# # Register your models here.
admin.site.register(Payment)
admin.site.register(OrderPlaced)
