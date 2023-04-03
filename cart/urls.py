from django.urls import path
from . import views

urlpatterns = [

  path('add_cart/<int:id>/',views.add_cart,name='add_cart'),
  path('view_cart',views.view_cart,name='view_cart'),
  path('de_cart/<int:id>/',views.de_cart,name='de_cart'),
  path('plusqty/<int:id>/',views.plusqty,name='plusqty'),
  path('minusqty/<int:id>/',views.minusqty,name='minusqty'),
  path('add_wishlist/<int:id>/',views.add_wishlist,name='add_wishlist'),
  path('view_wishlist',views.view_wishlist,name='view_wishlist'),
  path('de_wishlist/<int:id>/',views.de_wishlist,name='de_wishlist'),
  path('checkout',views.checkout,name='checkout'),
  path('paymentdone/', views.payment_done, name='paymentdone'),
  path('payment_success/', views.payment_success, name='payment_success'),
  path('pdf/<int:id>/', views.get,name='pdf'),
  path('sales_report/', views.sales_report, name='sales_report'),
]
