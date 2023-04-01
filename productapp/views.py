from django.shortcuts import redirect, render
from category.models import Category, Subcategory
from credentialapp.views import login
from django.contrib import messages
from productapp.models import Product, Productgallery, Sentiment, tbl_Review
from django.db.models import Sum




# Single product View .
def singleproduct(request,id):
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    # email = request.session['email']
    # review=tbl_Review.objects.filter(product=id).exclude(user_id=email)
    review=tbl_Review.objects.filter(product=id)
    count=tbl_Review.objects.filter(product=id).count()
    if "email" in request.session:
        email = request.session['email']
        user_review=tbl_Review.objects.filter(user_id=email,product=id)
        rate=tbl_Review.objects.filter(product=id)
        rating=0
        for i in rate:
            rating=rating+ i.rating
        if count == 0:
            total_rate=0.0
        else:
            total_rate=rating / count   
        product=Product.objects.get(id=id)
        image=Productgallery.objects.filter(product_id=id)
        data={'email':email,
              'total_rate':total_rate,
              'count':count,
              'product':product,
              'category':category,
              'subcategory':subcategory,
              'review':review,
              'image':image,
              'user_review':user_review
              }
        return render(request,"single-product.html",data)
    else:
        rate=tbl_Review.objects.filter(product=id)
        rating=0
        for i in rate:
            rating=rating+ i.rating
        if count == 0:
            total_rate=3.0
        else:
            total_rate=rating / count   
        product=Product.objects.get(id=id)
        image=Productgallery.objects.filter(product_id=id)
        data={'total_rate':total_rate,
              'count':count,
              'product':product,
              'category':category,
              'subcategory':subcategory,
              'review':review,
              'image':image
              }
        return render(request,"single-product.html",data)

# Customer Ratings
# def review(request,id):
#     if 'email' in request.session:
#         user=request.session['email'] 
#         product=Product.objects.get(id=id)
#         if request.method =="POST":
#             review=request.POST.get('message');
#             rate=request.POST.get('rate');
#             email=tbl_Review.objects.filter(user_id=user,product=id)
#             # if email :
#             #     return redirect(singleproduct,product.id)
#             # else:
#             if 'email' in request.session:
#                  # Perform sentiment analysis
#                 from nltk.sentiment.vader import SentimentIntensityAnalyzer
#                 sid = SentimentIntensityAnalyzer()
#                 scores = sid.polarity_scores(review)
#                 polarity_score = scores['compound']                
#                 # Update product sentiment score
#                 num_reviews = tbl_Review.objects.filter(product_id=product.id).count()
#                 avg_score = (product.sentiment_score * num_reviews + polarity_score) / (num_reviews + 1)
#                 product.sentiment_score = avg_score
#                 product.save()
#                 review=tbl_Review(user_id=user,product_id=product.id,review=review,rating=rate)
#                 review.save()
#                 sum = tbl_Review.objects.filter(product_id=product.id).aggregate(Sum('rating'))['rating__sum']
                
#             return redirect(singleproduct,product.id)
#     else:
#         return redirect(login)



def review(request,id):
    if 'email' in request.session:
        user=request.session['email'] 
        product=Product.objects.get(id=id)
        if request.method == "POST":
            review = request.POST.get('message')
            rate = request.POST.get('rate')
            product = Product.objects.get(id=id)

            # Perform sentiment analysis
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(review)

            # Get the polarity score for each sentiment
            negative_score = scores['neg']
            positive_score = scores['pos']
            neutral_score = scores['neu']

            # Save the review and rating to the database
            review = tbl_Review(user_id=user, product_id=product.id, review=review, rating=rate,positive_score=positive_score,negative_score=negative_score,neutral_score=neutral_score)
            review.save()
            from django.db.models import Avg
            reviews = tbl_Review.objects.filter(product_id=id)
            count=reviews.count()
            positive_avg=0
            negative_avg=0
            neutral_avg=0

            for i in reviews:
                positive_avg=positive_avg + i.positive_score
                negative_avg=negative_avg + i.negative_score
                neutral_avg=neutral_avg + i.neutral_score
            a=positive_avg/count * 100
            b=negative_avg/count * 100
            c=neutral_avg/count * 100
            sentiment_table=Sentiment.objects.filter(product_id=id)
            if sentiment_table:
                i=Sentiment.objects.get(product_id=id)
                i.num_reviews=count
                i.avg_pos_score=a
                i.avg_neg_score=b
                i.avg_neu_score=c
                i.save()
            else:
                Sentiment(product_id=id,avg_pos_score=a,avg_neg_score=b,avg_neu_score=c,num_reviews=count).save()
            return redirect(singleproduct, product.id)
    else:
        return redirect(login)