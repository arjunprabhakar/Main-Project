from django.urls import path
from . import views

urlpatterns = [
    path('',views.demo,name='demo'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('registration/',views.register,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('useraddress/',views.useraddress,name='useraddress'),
    path('de_address/<int:id>/',views.de_address,name='de_address'),
    path('edit_address',views.edit_address,name='edit_address'),
    path('change_password',views.change_password,name='change_password'),
    path('generateOTP',views.generateOTP,name='generateOTP'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('category_product/<int:id>/', views.category_product, name='category_product'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('verify_forgot_otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path('new_password/', views.new_password, name='new_password'),

]