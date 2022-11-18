from django.shortcuts import redirect, render
from category.models import Category, Subcategory
from credentialapp.views import login

from productapp.models import Product, tbl_Review

# Single product View .
def singleproduct(request,id):
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    review=tbl_Review.objects.filter(product=id)
    count=0
    for i in review:
        count=count+1
    if "email" in request.session:
        email = request.session['email']
        rate=tbl_Review.objects.filter(product=id)
        rating=0
        for i in rate:
            rating=rating+ i.rating
        if count == 0:
            total_rate=3.0
        else:
            total_rate=rating / count   
        product=Product.objects.filter(id=id)
        return render(request,"singleproduct.html",{'email':email,'total_rate':total_rate,'count':count,'product':product,'category':category,'subcategory':subcategory,'review':review})
    else:
        rate=tbl_Review.objects.filter(product=id)
        rating=0
        for i in rate:
            rating=rating+ i.rating
        if count == 0:
            total_rate=3.0
        else:
            total_rate=rating / count   
        product=Product.objects.filter(id=id)
        return render(request,"singleproduct.html",{'total_rate':total_rate,'count':count,'product':product,'category':category,'subcategory':subcategory,'review':review})

# Customer Ratings
def review(request,id):
    if 'email' in request.session:
        user=request.session['email'] 
        product=Product.objects.get(id=id)
        if request.method =="POST":
            review=request.POST.get('message');
            rate=request.POST.get('rate');
            review=tbl_Review(user_id=user,product_id=product.id,review=review,rating=rate) 
            review.save()
            return redirect(singleproduct,product.id)
        return redirect(login)