from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>/',views.singleproduct,name='singleproduct'),
    path('review/<int:id>/',views.review,name='review'),
]