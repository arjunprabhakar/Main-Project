from django.urls import path
from . import views
from .views import search_products

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
    path('search/', search_products, name='search_products'),
    path('category_product/<int:id>/', views.category_product, name='category_product'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('verify_forgot_otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path('new_password/', views.new_password, name='new_password'),


# Customer Service URLS
    path('View_Service/', views.View_Service, name='View_Service'),




    # Service Module URLS
    path('Service/', views.Service, name='Service'),
    path('Service_Profile/', views.Service_Profile, name='Service_Profile'),
    path('Service_Details/', views.Service_Details, name='Service_Details'),
    path('Service_Details_Update/', views.Service_Details_Update, name='Service_Details_Update'),
    path('Service_Product/', views.Service_Product, name='Service_Product'),
    path('Accept_Request/<int:id>/', views.Accept_Request, name='Accept_Request'),
    path('download_pdf/<int:id>/', views.download_pdf, name='download_pdf'),
    path('Service_Status/<int:id>/', views.Service_Status, name='Service_Status'),
    path('Apply_Leave/', views.Apply_Leave, name='Apply_Leave'),
    path('service_Bill/', views.service_Bill, name='service_Bill'),
    path('work_hour/', views.work_hour, name='work_hour'),
    path('remove_bill_data/<int:id>/', views.remove_bill_data, name='remove_bill_data'),
    path('download_bill/', views.download_bill, name='download_bill'),
    path('view_bill/<int:id>/', views.view_bill, name='view_bill'),
    path('send_email_with_bill/<int:id>/', views.send_email_with_bill, name='send_email_with_bill'),
    path('service_history/', views.service_history, name='service_history'),
    
    
    path('download_ServiceBill/<int:id>/', views.download_ServiceBill, name='download_ServiceBill'),
    path('servicer_change_password/', views.servicer_change_password, name='servicer_change_password'),


]