from django.shortcuts import render

# Create your views here.
from datetime import datetime
from urllib import response
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from category.models import Category, Subcategory
from productapp.models import Product
from .models import reg_user,log_user, user_address
from hashlib import sha256

import math, random
from django.core.mail import send_mail

# Create your views here.
def demo(request):
    request.session.flush()
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    product=Product.objects.all()
    return render(request,"index.html",{'category':category,'subcategory':subcategory,'product':product})

def login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['pass']
        password2 = sha256(password.encode()).hexdigest()
        user=log_user.objects.filter(email=email,password=password2,status=True)
        if user:
            user_details=log_user.objects.get(email=email,password=password2)
            email=user_details.email
            request.session['email']=email
            messages.success(request, 'Login successfully..!! Welcome to smartstore')
            return redirect('home')
           
        else:
            print("Invalid")
            messages.success(request, 'Email or Password Incorrect..!!')
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    return render(request,'login.html',{'category':category,'subcategory':subcategory})

# Function for OTP Generation
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
         a=OTP
     print("swdfghjk",a)
     return OTP

# User Registration
def register(request):
    if request.method=='POST':
        email=request.POST.get('email');
        password1 = request.POST.get('pwd');
        password2 = request.POST.get('cpwd');
        username = request.POST.get('nme');
        lastname = request.POST.get('lnme');
        phone = request.POST.get('phn');
        pswd=sha256(password2.encode()).hexdigest()

        if log_user.objects.filter(email=email).exists():
            user=log_user.objects.get(email=email) 
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'Smart Store',[email], fail_silently=False, html_message=htmlgen)
            user.otp=o;
            user.save()
            messages.success(request, 'Email already exist....!!!!')
            return redirect('login')    
        else:
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'Smart Store',[email], fail_silently=False, html_message=htmlgen)
            log=log_user(email=email,password=pswd,otp=o)
            log.save()

            userid=log_user.objects.get(email=email)
            user=reg_user(email_id=userid.email,name=username,lname=lastname,phone_no=phone)           
            user.save()  
            request.session['email']=email 
            # messages.success(request, 'Your registration is successfull... Please Login!!')
            return redirect('verify_otp')
    
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    # session=request.session['email']
    return render(request, 'registration.html',{'category':category,'subcategory':subcategory})
 
# Otp Verification
def verify_otp(request):
    if 'email' in request.session:
        # print('session',session)
        if request.method=='POST':
            otps = request.POST.get('otp');
            email = request.POST.get('email');
            session=request.session['email']
            if log_user.objects.filter(email=email,otp=otps): 
                user=log_user.objects.get(email=email)
                user.status=True;
                user.save()
                messages.success(request, 'Email is verified')
                return redirect('login')
            else:
                messages.success(request, 'Invalid Otp!!')
                return redirect('verify_otp')
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        session=request.session['email']
        return render(request, 'otp.html',{'category':category,'subcategory':subcategory,'session':session})
    else:
        return redirect(login)


#Customer Home Page
def home(request):
    if 'email' in request.session:
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        email = request.session['email']
        product=Product.objects.all()
        return render(request,'home.html',{'email':email,'category':category,'subcategory':subcategory,'product':product})
    messages.success(request, ' Please Login!!')
    return redirect(login)

# Customer Logout
def logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect(login)
    messages.success(request, 'Logout!!!')

    #profile page
def profile(request):
    if 'email' in request.session:
        email = request.session['email']
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        profile=reg_user.objects.all()
        address=user_address.objects.filter(user_id=email)
        return render(request,"profile.html",{'email':email,'category':category,'subcategory':subcategory,'profile':profile,'address':address})
    messages.success(request, 'Sign in..!!')
    return redirect(login)
   
def useraddress(request):
    if request.method=='POST':
        fname=request.POST.get('fname');
        lname=request.POST.get('lname');
        email=request.POST.get('email');
        phone = request.POST.get('phn');
        hname = request.POST.get('hname');
        street = request.POST.get('street');
        city = request.POST.get('city');
        district = request.POST.get('district');
        pin = request.POST.get('pin');
        print(fname)
        if 'email' in request.session:
            user=request.session['email'] 
            address=user_address(user_id=user,fname=fname,lname=lname,email=email,phone_no=phone,hname=hname,street=street,city=city,district=district,pin=pin)
            address.save()
            messages.success(request, 'Address Added Successfully...')
            return redirect('profile')
        return redirect('profile')

# Edit Address
def edit_address(request):
       if 'email' in request.session:
            user=request.session['email'] 
            address=user_address.objects.get(user_id=user)
            if request.method =="POST":
                fname=request.POST.get('fname');
                lname=request.POST.get('lname');
                email=request.POST.get('email');
                phone = request.POST.get('phn');
                hname = request.POST.get('hname');
                street = request.POST.get('street');
                city = request.POST.get('city');
                district = request.POST.get('district');
                pin = request.POST.get('pin');

                address.fname=fname
                address.lname=lname
                address.email=email
                address.phone_no=phone
                address.hname=hname
                address.street=street
                address.city=city
                address.district=district
                address.pin=pin
                address.save()
                return redirect('profile')
            return redirect('login')


# Remove drress From 
def de_address(request,id):
    user_address.objects.get(id=id).delete()
    return redirect('profile')

def change_password(request):
    if 'email' in request.session:
        email=request.session['email']
        user=log_user.objects.get(email=email)
        if request.method =="POST":
            old_password=request.POST.get('oldpass')
            new_password=request.POST.get('pass');
            new_pswd=sha256(new_password.encode()).hexdigest()
            pswd=sha256(old_password.encode()).hexdigest()

            if pswd == user.password:
                user.password=new_pswd
                user.save()
                print("Password updated Successfully")
                messages.success(request, 'Password updated Successfully...')
                return redirect('profile')
            else:
                messages.success(request, 'Incorrect Password ...')
                print("Incorrect Password")
                return redirect('profile')
        return redirect('login')






            


