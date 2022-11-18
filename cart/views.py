from asyncio.windows_events import NULL
from django.shortcuts import render,redirect
from category.models import Category, Subcategory
from credentialapp.models import log_user, user_address
from productapp.models import Product
from django.contrib import messages
from credentialapp.views import login
from .models import Cart, Wishlist
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
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        email = request.session['email']
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        return render(request,"checkout.html",{'cart_count':cart_count,'email':email,'category':category,'subcategory':subcategory,'address':address,'item':item,'total':total})
    return redirect(login)