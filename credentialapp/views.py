from io import BytesIO
from django.shortcuts import render

# Create your views here.
from datetime import datetime
from urllib import response
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from cart.models import Cart, OrderPlaced
from category.models import Category, Subcategory
from productapp.models import Product, tbl_Review
from .models import Servicer_Details, Servicer_Product, reg_user,log_user, tbl_Accepted_product, tbl_Accepted_product_status, tbl_ServiceBill, user_address
from hashlib import sha256

# For Pdf Download
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import math, random
from django.core.mail import send_mail

# Create your views here.
def demo(request):
    request.session.flush()
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    product=Product.objects.all()
    context={'category':category,
             'subcategory':subcategory,
             'product':product}
    return render(request,"Customer/index.html",context)

# Login Form
def login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['pass']
        password2 = sha256(password.encode()).hexdigest()
        user=log_user.objects.filter(email=email,password=password2,status=True,type=0)
        user2=log_user.objects.filter(email=email,password=password2,status=True,type=1)
        if user:
            user_details=log_user.objects.get(email=email,password=password2)
            email=user_details.email
            request.session['email']=email
            messages.success(request, 'Login successfully..!! Welcome to smartstore')
            return redirect('home')
        elif user2:
            user_details=log_user.objects.get(email=email,password=password2,type=1)
            email=user_details.email
            request.session['email']=email
            messages.success(request, 'Login successfully..!! Welcome to smartstore Service Team')
            return redirect('Service')     
        else:
            messages.success(request, 'Email or Password Incorrect..!!')
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    context={'category':category,
             'subcategory':subcategory}
    return render(request,'Customer/login.html',context)

# Function for OTP Generation
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
         a=OTP
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

        if log_user.objects.filter(email=email,status=True).exists():
            messages.success(request, 'Email already exist....!!!!')
            return redirect('login') 
        elif log_user.objects.filter(email=email,status=False).exists():
            user=log_user.objects.get(email=email) 
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'Smart Store',[email], fail_silently=False, html_message=htmlgen)
            user.otp=o;
            user.save()
            request.session['email']=email 
            messages.success(request, 'Email already exist..Please Verify Email!!!!')
            return redirect('verify_otp') 
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
    context={'category':category,
             'subcategory':subcategory}
    return render(request, 'Customer/registration.html',context)
 
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
        context={'category':category,
                 'subcategory':subcategory,
                 'session':session}
        return render(request, 'Customer/otp.html',context)
    else:
        return redirect(login)


#Customer Home Page
def home(request):
    if 'email' in request.session:
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        email = request.session['email']
        product=Product.objects.all()
        review=tbl_Review.objects.all()
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        context={'cart_count':cart_count,
                 'email':email,
                 'category':category,
                 'subcategory':subcategory,
                 'product':product}
        return render(request,'Customer/home.html',context)
    messages.success(request, ' Please Login!!')
    return redirect(login)

#Customer Logout
def logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect(login)
    messages.success(request, 'Logout!!!')

#profile page
def profile(request):
    if 'email' in request.session:
        email = request.session['email']
        address=user_address.objects.filter(user_id=email)
        order=OrderPlaced.objects.filter(user_id=email)
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        service_product=Servicer_Product.objects.filter(user_id=email)
        user=reg_user.objects.get(email_id=email)
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        data={'cart_count':cart_count,
              'email':email,
              'category':category,
              'subcategory':subcategory,
              'address':address,
              'user':user,
              'order':order,
              'service_product':service_product,}
        return render(request,"Customer/profile.html",data)
    messages.success(request, 'Sign in..!!')
    return redirect(login)

# Add Shipping Address
def useraddress(request):
    if request.method=='POST':
        fname=request.POST.get('fname');
        lname=request.POST.get('lname');
        email=request.POST.get('email');
        phone = request.POST.get('phn');
        state = request.POST.get('state');
        district = request.POST.get('district');
        hname = request.POST.get('hname');
        street = request.POST.get('street');
        city = request.POST.get('city');
        pin = request.POST.get('pin');
        print(fname)
        if 'email' in request.session:
            user=request.session['email']
            count=user_address.objects.filter(user_id=user).count() 
            if count >= 3:
                messages.success(request, 'Please Remove The Existing Address then add new address..!')
                return redirect(profile)
            else:
                address=user_address(user_id=user,fname=fname,lname=lname,email=email,phone_no=phone,hname=hname,street=street,city=city,district=district,state=state,pin=pin)
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

# Change Password
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


# Product Search 
def searchbar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            multiple_q = Q(Q(name__icontains=query) | Q( description__icontains=query))
            products = Product.objects.filter(multiple_q) 
            category=Category.objects.all()
            subcategory=Subcategory.objects.all()
            if 'email' in request.session:
                email = request.session['email']
                context={'product':products,
                         'category':category,
                         'subcategory':subcategory,
                         'email':email}
                return render(request, 'Customer/search.html',context)
            else:
              context={'product':products,
                       'category':category,
                       'subcategory':subcategory}
              return render(request, 'Customer/search.html',context)  
        else:
            messages.info(request, 'No search result!!!')
            print("No information to show")
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    if 'email' in request.session:
        email = request.session['email']
        context={'category':category,
                 'subcategory':subcategory,
                 'email':email}
        return render(request, 'Customer/search.html',context)
    else:
        context={'category':category,
                 'subcategory':subcategory}
        return render(request, 'Customer/search.html',context)


from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.urls import reverse


def search_products(request):
    query = request.GET.get('query')
    if query:
        multiple_q = Q(Q(name__icontains=query))
        products = Product.objects.filter(multiple_q)
    else:
        products = Product.objects.none()
    product_list = []
    for p in products:
        product = {
            'id': p.id,
            'name': p.name,
            # 'image_url': None,
            'url': request.build_absolute_uri(reverse('singleproduct', args=[p.id])),
        }
        if p.image:
            image_url = settings.MEDIA_URL + str(p.image)
            product['image_url'] = request.build_absolute_uri(image_url)
            
        product_list.append(product)

    return JsonResponse({'products': product_list})


# Category wise product filtering
def category_product(request,id):
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    sub_category=Subcategory.objects.get(id=id)
    if "email" in request.session:
        email = request.session['email']
        product=Product.objects.filter(subcategory=id)
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        context={'sub_category':sub_category,
                 'cart_count':cart_count,
                 'product':product,
                 'category':category,
                 'subcategory':subcategory,
                 'email':email}
        return render(request,'Customer/category.html',context)
    else:
        product=Product.objects.filter(subcategory=id)
        context={'sub_category':sub_category,
                 'product':product,
                 'category':category,
                 'subcategory':subcategory}
        return render(request,'Customer/category.html',context)
            
# Forgot Password
def forgotpassword(request):
    if request.method =="POST":
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        email=request.POST.get('email')
        if log_user.objects.filter(email=email).exists():
            user=log_user.objects.get(email=email) 
            o=generateOTP()
            htmlgen = '<p>Your OTP is:'+o+'</p>'
            send_mail('OTP request',o,'Smart Store',[email], fail_silently=False, html_message=htmlgen)
            user.otp=o;
            user.save()
            request.session['email']=email 
            messages.success(request, 'OTP is send to ..'+email+'...Please Verify')
            return redirect('verify_forgot_otp')
        else:
            messages.success(request, 'Email Not Exist ...')
            return redirect(login)
    context={'category':category,
             'subcategory':subcategory}
    return render(request,'Customer/forgotpassword.html',context)

# Verify forgot password OTP
def verify_forgot_otp(request):
    if 'email' in request.session:
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        if request.method=='POST':
            otps = request.POST.get('otp');
            email = request.POST.get('email');
            if log_user.objects.filter(email=email,otp=otps):
                messages.success(request, 'OTP is Verified..Please Enter New Password...')
                return redirect(new_password)
            else:
                 messages.success(request, 'Incorrcect OTP...')
    session=request.session['email']
    context={'session':session,
             'category':category,
             'subcategory':subcategory}
    return render(request,'Customer/verify_forgot_otp.html',context)

# New Password via Forgot Password
def new_password(request):
    if 'email' in request.session:
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        if request.method=='POST':
            password = request.POST.get('pswd');
            pswd=sha256(password.encode()).hexdigest()
            email = request.POST.get('email');
            user=log_user.objects.get(email=email)
            user.password=pswd
            user.save()
            messages.success(request, 'Password Updated Successfully ...')
            return redirect(login)
    session=request.session['email']
    context={'session':session,
             'category':category,
              'subcategory':subcategory,}
    return render(request,'Customer/newpassword.html',context)





# *********************************** Customer Service Functions **********************************





def View_Service(request):
    if 'email' in request.session:
        user=request.session['email']
        if request.method=='POST':
            cat = request.POST.get('category');
            brand = request.POST.get('brand');
            model = request.POST.get('model');
            model_no = request.POST.get('model_no');
            waranty = request.POST.get('waranty');
            bill = request.FILES.get('bill');
            issue = request.POST.get('issue');
            Servicer_Product(user_id=user,category=cat,brand=brand,
                             model=model,model_no=model_no,waranty=waranty,bill=bill,issues=issue).save()
        return redirect(profile)
    else:
        return redirect(login)






#  ******************************************* Service Module Functions ******************************


# Service Home Page
def Service(request):
    if 'email' in request.session:
        email=request.session['email']
        user=log_user.objects.get(email=email)
        user_details=Servicer_Details.objects.filter(user_id=email)
        status=Servicer_Details.objects.get(user_id=email)
        rqst=Servicer_Product.objects.filter(status=0)
        accepted_rqst=tbl_Accepted_product.objects.filter(Servicer_id=email,status=0)
        data={'user':user,
              'email':email,
              'rqst':rqst,
              'user_details':user_details,
              'status':status,
              'accepted_rqst':accepted_rqst}
        return render(request,"Service/Service_Index.html",data)
    else:
        return redirect(login)

    

# Service Profile
def Service_Profile(request):
    if 'email' in request.session:
        category=Category.objects.all()
        email=request.session['email']
        user=Servicer_Details.objects.filter(user_id=email)
        count=Servicer_Details.objects.filter(user_id=email).count()
        data={
            'email':email,
            'user':user,
            'count':count,
            'category':category,
        }
        return render(request,"Service/Service_Profile.html",data)
    else:
        return redirect(login)
    

# Servicer Details Add
def Service_Details(request):
    if 'email' in request.session:
        email=request.session['email']
        if request.method=='POST':
            fname = request.POST.get('fname');
            lname = request.POST.get('lname');
            phone = request.POST.get('phone');
            category = request.POST.get('category');
            hname = request.POST.get('hname');
            street = request.POST.get('street');
            city = request.POST.get('city');
            district = request.POST.get('district');
            pin = request.POST.get('pin');
            img = request.FILES.get('img');
            Servicer_Details(user_id=email,fname=fname,lname=lname,phone_no=phone,hname=hname,
                             street=street,city=city,district=district,pin=pin,image=img,category_id=category).save()
            return redirect(Service_Profile)
    else:
        return redirect(login)
    
# Servicer Details Edit
def Service_Details_Update(request):
    if 'email' in request.session:
        email=request.session['email']
        if request.method=='POST':
            fname = request.POST.get('fname');
            lname = request.POST.get('lname');
            phone = request.POST.get('phone');
            hname = request.POST.get('hname');
            street = request.POST.get('street');
            city = request.POST.get('city');
            district = request.POST.get('district');
            pin = request.POST.get('pin');
            user=Servicer_Details.objects.get(user_id=email)
            user.fname=fname
            user.lname=lname
            user.phone_no=phone
            user.hname=hname
            user.street=street
            user.city=city
            user.district=district
            user.pin=pin
            user.save()
            return redirect(Service_Profile)
    else:
        return redirect(login)
    
# Servicer main page for the  Accepted request (that is for main service page)
def Service_Product(request):
    if 'email' in request.session:
        email=request.session['email']
        user=log_user.objects.filter(email=email)
        product=tbl_Accepted_product.objects.filter(Servicer_id=email,status=0)
        status=tbl_Accepted_product_status.objects.order_by('-id')
        service_bill=tbl_ServiceBill.objects.filter(Servicer_id=email,status=0)
        count=tbl_ServiceBill.objects.filter(Servicer_id=email,status=0).count()
        if product:
            data={
                'user':user,
                'product':product,
                'status':status,
                'bill':service_bill,
                'count':count,
            }

            return render(request,"Service/Service_Product.html",data)
        else:
            messages.success(request, 'You have no active work...!!')
            return redirect(Service)
    else:
        return redirect(login)



# Servicer Accept Request
def Accept_Request(request,id):
    if 'email' in request.session:
        user=request.session['email']
        servicer=tbl_Accepted_product.objects.filter(Servicer_id=user,status=0)
        if servicer:
            messages.success(request, 'Accept only one task at a time..!')
            return redirect(Service)
        else:
            tbl_Accepted_product(Servicer_id=user,product_id=id).save()
            rqst=Servicer_Product.objects.get(id=id)
            rqst.status=1
            rqst.save()
            messages.success(request, 'Service request accepted successfully..!')
            return redirect(Service_Product)
    else:
        return redirect(login)
    




# pdf bill download by servicer
def download_pdf(request, id):
    pdf_file = get_object_or_404(Servicer_Product, id=id)
    return FileResponse(pdf_file.bill, as_attachment=True)

def Service_Status(request,id):
    if 'email' in request.session:
        user=request.session['email']
        if request.method=='POST':
            status_head = request.POST.get('status_head');
            status_msg = request.POST.get('status_msg');
            tbl_Accepted_product_status(Servicer_id=id,status_head=status_head,status_message=status_msg).save()
            return redirect(Service_Product)
    else:
        return redirect(login)
    

# for apply leave
def Apply_Leave(request):
    if 'email' in request.session:
        return render(request,'Service/apply_leave.html')
    else:
        return redirect(login)


# function for generate service bill
def service_Bill(request):
    if 'email' in request.session:
        email=request.session['email']
        user=log_user.objects.get(email=email)
        if request.method=='POST':
            product=request.POST.get('product')
            spare=request.POST.getlist('spare')
            amount=request.POST.getlist('amount')
            for i in range(len(spare)):
                    tbl_ServiceBill(Servicer_id=user,Accepted_product_id=product,sparepart=spare[i],amount=amount[i]).save()
        return redirect(Service_Product)
    else:
        return redirect(login)
    

# function for remove the data from the bill table
def remove_bill_data(request,id):
    if 'email' in request.session:
        tbl_ServiceBill.objects.get(id=id).delete()
        return redirect(Service_Product)
    else:
        return redirect(login)
    



# for updating the total work hour
def work_hour(request):
    if 'email' in request.session:
        email=request.session['email']
        if request.method=='POST':
            time=request.POST.get('hour')
            product=request.POST.get('product')
            products=tbl_Accepted_product.objects.get(Servicer_id=email,id=product)
            products.work_hour=time
            products.save()
        return redirect(Service_Product)
    else:
        return redirect(login)




from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def download_bill(request):

    # Render the HTML template
    template = get_template('Service/bill.html')
    html = template.render({'foo': 'bar'})
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Convert HTML to PDF using xhtml2pdf
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), buffer)

    # If PDF generation failed, return an error response
    if pdf.err:
        return HttpResponse('PDF generation failed', status=500)

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
    return response






import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from datetime import date
from django.db.models import Q

def view_bill(request,id):
    accepted_product=tbl_Accepted_product.objects.get(id=id,status=0)
    service_bill=tbl_ServiceBill.objects.filter(Accepted_product=accepted_product.product_id).count()
    print(service_bill,'##############')
    if accepted_product.work_hour != 0 or service_bill != "" :
        # Retrieve all service bill instances
        bills = tbl_ServiceBill.objects.filter(Accepted_product=accepted_product.product_id)

        # Create a PDF buffer using StringIO
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file"
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Define the invoice details
        pdf.setFillColorRGB(0.3, 0.3, 0.3)
        pdf.rect(50, 720, 500, 50, fill=True, stroke=False)

        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(300, 750, "Smart Store")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(260, 730, "Service Invoice")
        pdf.setFont("Helvetica", 7)
        pdf.drawString(450, 750, "phone : 8301014276")
        pdf.drawString(450, 740, "Email : smartstore@gmail.com")

        # Draw the date on the right side of the page outside the rectangle
        today = date.today().strftime("%B %d, %Y")
        pdf.setFillColorRGB(0, 0, 0)  # Set text color to blue
        pdf.setFont("Helvetica", 10)
        pdf.drawRightString(150, 688, f"Date: {today}")

        pdf.setFillColorRGB(0, 0, 0)  # Set text color to blue
        pdf.setFont("Helvetica", 10)
        pdf.drawRightString(530, 688, f"Customer Name: Arjun P P")
        pdf.drawRightString(530, 676, f"Phone: 8301014273")
        pdf.drawRightString(530, 664, f"Email: arjun@gmail.com")
        
        pdf.setFillColorRGB(0, 0, 0)  # Set text color to blue
        pdf.setFont("Helvetica", 14)
        pdf.drawRightString(355,610, f"")

        col_widths = [50, 150, 100, 100]   
        # Define the table headings
        table_data = [["#","Spare","Rate","Quantity","Amount"]]
        table_data.append(['','','',''])

        total_amount=0
        # Add the service bill details to the table
        for i, bill in enumerate(bills):
            product = bill.Accepted_product.brand
            sparepart = bill.sparepart
            rate = bill.amount
            amount=rate * 2
            serial_number = i + 1
            total_amount=total_amount+amount
            table_data.append([serial_number,sparepart,rate,'2',amount])

        table_data.append(['', '', '','',''])
        table_data.append(['----------------', '----------------------------------------', '----------------------------------','------------------------------','------------------------'])

        table_data.append(['', '', '', 'Total Amount:', total_amount])
        table_data.append(['', '', '',''])
        table_data.append(['','','','Labour Charge:','2000.00'])
        table_data.append(['','','',''])
    
        table_data.append(['','','','Grand Total:','20000.00'])


        # Create the table
        t = Table(table_data,colWidths=col_widths)

        # Add style to the table
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#e8e8e8'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('TEXTCOLOR', (0, -1), (-1, -1),'#FF723D'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
            ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        # Get the table width and height
        w, h = t.wrapOn(pdf, 550, 500)

        # Draw the table on the PDF
        t.drawOn(pdf, 50, 600 - h)
        # Close the PDF object cleanly, and we're done
        pdf.showPage()
        pdf.save()

        from django.core.files.base import ContentFile
        from io import BytesIO
        accepted_product = tbl_Accepted_product.objects.get(id=id)

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        accepted_product.service_bill.save('invoice.pdf', ContentFile(pdf_bytes))
            
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    else:
        messages.success(request, 'First add invoice details..!')
        return redirect(Service_Product)




from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os

def send_email_with_bill(request, id):
    # Get the accepted product object
    accepted_product = tbl_Accepted_product.objects.get(id=id)
    # Set up the email message
    subject = 'Smart Store Service Bill'
    message = 'Dear Sir,\nWe hope this email finds you well.we are sending you the bill for the product service you have purchased from us.\n We appreciate your business and would like to thank you for choosing our Smart Store for your needs.\nPlease find the attached invoice.\nBest regards,\nSmart Store.\nEmail : smartstore@gmail.com\nphone:8798678898\n'
    from_email = settings.EMAIL_HOST_USER
    # recipient_list = 'arjunpp2023a@mca.ajce.in'  # Replace with the recipient email address
    recipient_list = [accepted_product.Servicer.email]  # Replace with the recipient email address
    email = EmailMessage(subject, message, from_email, recipient_list)

    # Add the service bill attachment
    if accepted_product.service_bill:
        email.attach_file(accepted_product.service_bill.path)

    # Send the email
    try:
        accepted_product.status=1
        accepted_product.work_done=1
        accepted_product.save()
        bill=tbl_ServiceBill.objects.filter(Accepted_product_id=accepted_product.product_id)
        print(accepted_product.id,'##################')
        for i in bill:
            i.status=1
            i.save()
        email.send()
        messages.success(request, 'Successfully the work Finished ..!')
        return redirect(Service)
    except Exception as e:
        return HttpResponse('Error sending email: {}'.format(str(e)))





# for view the service history of a servicer
def service_history(request):
    if 'email' in request.session:
        user=request.session['email']
        work=tbl_Accepted_product.objects.filter(Servicer_id=user,work_done=1)
        data={'work':work}
        return render(request,'Service/service_history.html',data)
    else:
        return redirect(login)
    


# servicer download the service bill
def download_ServiceBill(request,id):
    if 'email' in request.session:
        pdf_file = get_object_or_404(tbl_Accepted_product, id=id)
        return FileResponse(pdf_file.service_bill, as_attachment=True)
    else:
        return redirect(login)
    



# Change Password
def servicer_change_password(request):
    if 'email' in request.session:
        email=request.session['email']
        user=log_user.objects.get(email=email)
        if request.method =="POST":
            old_password=request.POST.get('oldpass')
            new_password=request.POST.get('newpass');
            new_pswd=sha256(new_password.encode()).hexdigest()
            pswd=sha256(old_password.encode()).hexdigest()

            if pswd == user.password:
                user.password=new_pswd 
                user.save()
                print("Password updated Successfully")
                messages.success(request, 'Password updated Successfully...')
                return redirect('Service_Profile')
            else:
                messages.success(request, 'Incorrect Password ...')
                print("Incorrect Password")
                return redirect('Service_Profile')
        return redirect('login')
