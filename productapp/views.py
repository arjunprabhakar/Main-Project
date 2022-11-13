from django.shortcuts import render

from productapp.models import Product

# Create your views here.

def singleproduct(request,id):
    product=Product.objects.filter(id=id)
    return render(request,"singleproduct.html",{'product':product})

