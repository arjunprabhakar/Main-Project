from asyncio.windows_events import NULL
from django.conf import settings
from django.shortcuts import render,redirect
import razorpay
from category.models import Category, Subcategory
from credentialapp.models import log_user, user_address
from productapp.models import Product
from django.contrib import messages
from credentialapp.views import login
from .models import Cart, OrderPlaced, Payment, Wishlist
from django.contrib import messages

# Cart functions
def add_cart(request,id):
    if 'email' in request.session:
        item=Product.objects.get(id=id)
        user=request.session['email'] 
        if item.stock>0:
            item.stock -=1
            if Cart.objects.filter( user_id =user,product_id=item).exists():
                c_item=Cart.objects.get( user_id =user,product_id=item)
                c_item.product_qty = c_item.product_qty + 1
                c_item.save()
                return redirect('view_cart')
            else:
                product_qty = 1
                price= item.price * product_qty
                new_cart=Cart(user_id=user,product_id=item.id,product_qty=product_qty,price=price)
                new_cart.save()
                return redirect('view_cart')
    messages.success(request, 'Sign in..!!')
    return redirect(login)

# Cart Quentity Plus Settings
def plusqty(request,id):
    cart=Cart.objects.filter(id=id)
    
    for cart in cart:   
        if cart.product.stock > cart.product_qty:
            cart.product_qty +=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect('view_cart')
        # messages.success(request, 'Out of Stock')
        return redirect('view_cart')

# Cart Quentity Plus Settings
def minusqty(request,id):
    cart=Cart.objects.filter(id=id)
    for cart in cart:
        if cart.product_qty > 1 :
            cart.product_qty -=1
            cart.price=cart.product_qty * cart.product.price
            cart.save()
            return redirect('view_cart')
        return redirect('view_cart')


#Cart View page
def view_cart(request):  
    if 'email' in request.session:
        email = request.session['email']
        cart=Cart.objects.filter(user_id=email)
        total = 0
        for item in cart:
            total +=  item.product.price * item.product_qty
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        return render(request,"cart.html",{'cart_count':cart_count,'cart':cart,'email':email,'total':total,'category':category,'subcategory':subcategory})
    return redirect(login)
    
# Remove Items From Cart
def de_cart(request,id):
    Cart.objects.get(id=id).delete()
    return redirect('view_cart')


# add to wishlist 
def add_wishlist(request,id):
    if 'email' in request.session:
        item=Product.objects.get(id=id)
        user=request.session['email']       
        if Wishlist.objects.filter( user_id =user,product_id=item).exists():
            return redirect('view_wishlist')        
        else:
            new_wishlist=Wishlist(user_id=user,product_id=item.id)
            new_wishlist.save()
            return redirect('view_wishlist')
    messages.success(request, 'Sign in..!!')
    return redirect(login)
    


#Wishlist View page
def view_wishlist(request):  
    if 'email' in request.session:
        email = request.session['email']
        cart=Wishlist.objects.filter(user_id=email)
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        return render(request,"wishlist.html",{'cart_count':cart_count,'cart':cart,'email':email,'category':category,'subcategory':subcategory})
    return redirect(login)

# Remove Items From Wishlist
def de_wishlist(request,id):
    Wishlist.objects.get(id=id).delete()
    return redirect('view_wishlist')


def checkout(request):
    if 'email' in request.session:
        email = request.session['email']
        address=user_address.objects.filter(user_id=email)
        item=Cart.objects.filter(user_id=email)
        total = 0
        for i in item:
            total +=  i.product.price * i.product_qty
        stotal=total * 100
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        email = request.session['email']
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
        data = {
        "amount": 100,
        "currency": "INR",
        }
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_KiA1Iabwcd5AhC', 'entity': 'order', 'amount': 100, 'amount_paid': 0, 'amount_due': 100, 'currency': 'INR', 'receipt': None, 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1668918385}
        order_id = payment_response['id']
        request.session['order_id'] = order_id
        order_status = payment_response['status']
        email = request.session['email']
        users=log_user.objects.get(email=email)
        if order_status == 'created':
            payment = Payment(person=users,amount=total,razorpay_order_id = order_id,razorpay_payment_status = order_status)
        payment.save()
        return render(request,"checkout.html",{'stotal':stotal,'cart_count':cart_count,'email':email,'category':category,'subcategory':subcategory,'address':address,'item':item,'total':total})
    return redirect(login)

def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    payment=Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    # customer=Address_Book.objects.get(user=request.user,status=True)
    email = request.session['email']
    person=log_user.objects.get(email=email)
    cart=Cart.objects.filter(user=email)
    # item = Product.objects.get(product=product, id=item_id)
    for c in cart:
        OrderPlaced(user=person,product=c.product,quantity=c.product_qty,payment=payment,is_ordered=True).save()
        pro=Product.objects.get(id = c.product.id)
        pro.stock=pro.stock - c.product_qty
        pro.save()
        c.delete()
    return redirect(payment_success)

# Payment Success Page
def payment_success(request): 
    if 'email' in request.session:
        email=request.session['email']
        address=user_address.objects.filter(user_id=email)
        order=OrderPlaced.objects.filter(user_id=email)
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        return render(request,"Payment_Success.html",{'email':email,'address':address,'order':order,'category':category,'subcategory':subcategory})
    else:
        return redirect(login)