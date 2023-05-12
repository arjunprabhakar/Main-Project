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
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
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
                price= item.selling_price * product_qty
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
            cart.price=cart.product_qty * cart.product.selling_price
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
            cart.price=cart.product_qty * cart.product.selling_price
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
            total +=  item.product.selling_price * item.product_qty
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        return render(request,"Customer/cart.html",{'cart_count':cart_count,'cart':cart,'email':email,'total':total,'category':category,'subcategory':subcategory})
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
        carts=Wishlist.objects.filter(user_id=email)
        category=Category.objects.all()
        subcategory=Subcategory.objects.all()
        cart=Cart.objects.filter(user_id=email)
        cart_count=0
        for i in cart:
            cart_count=cart_count+ i.product_qty
        return render(request,"Customer/wishlist.html",{'cart_count':cart_count,'carts':carts,'cart':cart,'email':email,'category':category,'subcategory':subcategory})
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
            total +=  i.product.selling_price * i.product_qty
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
        return render(request,"Customer/checkout.html",{'stotal':stotal,'cart_count':cart_count,'email':email,'category':category,'subcategory':subcategory,'address':address,'item':item,'total':total})
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
        return render(request,"Customer/PaymentSuccess.html",{'email':email,'address':address,'order':order,'category':category,'subcategory':subcategory})
    else:
        return redirect(login)
    

# For Product Order Bill 
def get(request,id,*args, **kwargs,):
    if 'email' in request.session:   
        email=request.session['email'] 
        place = OrderPlaced.objects.get(id=id)
        date=place.payment.created_at
        orders=OrderPlaced.objects.filter(user_id=email,payment__created_at=date)
        address=user_address.objects.filter(user_id=email)
        total=0
        for o in orders:
            total=total+(o.product.selling_price*o.quantity)
        # addrs=user_address.objects.get(user_id=request.user.id)
        data = {
            "total":total,
            "orders":orders,
            "address":address,

        }
        pdf = render_to_pdf('report.html',data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            filename = "Bill"
            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found")
    


# views.py

# from django.shortcuts import render
# import matplotlib.pyplot as plt
# from django.db.models import Count
# from django.shortcuts import render
# from .models import OrderPlaced
# from django.db.models.functions import TruncDate
# import base64
# import io

# def my_page(request):
#     # Your view code here
#     orders_by_date = OrderPlaced.objects.filter(is_ordered=True).annotate(date=TruncDate('ordered_date')).values('date').annotate(count=Count('id'))
#     dates = [d['date'] for d in orders_by_date]
#     counts = [d['count'] for d in orders_by_date]
#     plt.plot(dates, counts)
#     plt.title('Sales Graph')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Orders')
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     graph = plt.gcf()
#     buf = io.BytesIO()
#     graph.savefig(buf, format='png')
#     buf.seek(0)
#     graph_image = base64.b64encode(buf.read()).decode('utf-8')
#     plt.close()
#     context = {'graph_image': graph_image}
#     context = {
#         'graph_image': graph_image
#     }
#     return render(request, 'my_template.html', context)
import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import OrderPlaced

from django.db.models.functions import TruncDate
from django.db.models import Count
import io
import base64
import matplotlib.pyplot as plt

from django.db.models.functions import TruncDate
from django.db.models import Count
import matplotlib.pyplot as plt
import base64
import io
from .models import OrderPlaced
from datetime import datetime, timezone
from django.db.models import Sum




def sales_report(request):
    current_month = datetime.now().month
    type1 = request.GET.get('category_option')
    type2 = request.GET.get('single_option')
    type3 = request.GET.get('custom_option')
    category = request.GET.get('category')
    sinle_date = request.GET.get('single_date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if category == '1000' :
        orders = OrderPlaced.objects.all()
    else:
        orders = OrderPlaced.objects.filter(product__category=category, is_ordered=True)


    product_data = {}
    for order in orders:
        product_name = order.product.name
        product_total = order.total_cost() * order.quantity
        if product_name in product_data:
            product_data[product_name]['quantity'] += order.quantity
            product_data[product_name]['total'] += product_total
        else:
            product_data[product_name] = {
                'quantity': order.quantity,
                'total': product_total,
            }

    data = []
    for name, values in product_data.items():
        data.append({
            'name': name,
            'quantity': values['quantity'],
            'total': values['total'],
        })

    total_sales = sum([item['total'] for item in data])
    datas=1
    category=Category.objects.all()
    context = {
        'product_data': data,
        'total_sales': total_sales,
        'data':datas,
        'category':category,
    }
    return render(request, 'sales_analysis.html', context)





