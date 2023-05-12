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
        return render(request,"Customer/singleproduct.html",data)






# from textblob import TextBlob

# def review(request, id):
#     if 'email' in request.session:
#         user = request.session['email']
#         product = Product.objects.get(id=id)
#         if request.method == "POST":
#             review = request.POST.get('message')
#             rate = request.POST.get('rate')
#             product = Product.objects.get(id=id)

#             # Perform sentiment analysis
#             blob = TextBlob(review)
#             polarity_score = blob.sentiment.polarity
#             subjectivity_score = blob.sentiment.subjectivity

#             # Get the polarity score for each sentiment
#             if polarity_score > 0:
#                 positive_score = polarity_score
#                 negative_score = 0
#             elif polarity_score < 0:
#                 positive_score = 0
#                 negative_score = abs(polarity_score)
#             else:
#                 positive_score = 0
#                 negative_score = 0

#             # Save the review and rating to the database
#             review = tbl_Review(user_id=user, product_id=product.id, review=review, rating=rate, positive_score=positive_score, negative_score=negative_score)
#             review.save()

#             # Update the sentiment table
#             reviews = tbl_Review.objects.filter(product_id=id)
#             count = reviews.count()
#             positive_avg = 0
#             negative_avg = 0
#             # neutral_avg=0

#             for i in reviews:
#                 positive_avg=positive_avg + i.positive_score
#                 negative_avg=negative_avg + i.negative_score
#                 # neutral_avg=neutral_avg + i.neutral_score
#             a=positive_avg/count * 100
#             b=negative_avg/count * 100
#             # c=neutral_avg/count * 100
#             sentiment_table=Sentiment.objects.filter(product_id=id)
#             if sentiment_table:
#                 i=Sentiment.objects.get(product_id=id)
#                 i.num_reviews=count
#                 i.avg_pos_score=a
#                 i.avg_neg_score=b
#                 # i.avg_neu_score=c
#                 i.save()
#             else:
#                 Sentiment(product_id=id,avg_pos_score=a,avg_neg_score=b,num_reviews=count).save()
#             return redirect(singleproduct, product.id)
#     else:
#         return redirect(login)






from textblob import TextBlob
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt


def review(request, id):
    if 'email' in request.session:
        user = request.session['email']
        product = Product.objects.get(id=id)
        if request.method == "POST":
            review = request.POST.get('message')
            rate = request.POST.get('rate')
            product = Product.objects.get(id=id)

            # Perform sentiment analysis
            blob = TextBlob(review)
            polarity_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity
            print(subjectivity_score,'############')

            # Get the polarity score for each sentiment
            if polarity_score > 0:
                positive_score = polarity_score
                negative_score = 0
            elif polarity_score < 0:
                positive_score = 0
                negative_score = abs(polarity_score)
            else:
                positive_score = 0
                negative_score = 0

            # Save the review and rating to the database
            review = tbl_Review(user_id=user, product_id=product.id, review=review, rating=rate, positive_score=positive_score, negative_score=negative_score)
            review.save()

            # Update the sentiment table
            reviews = tbl_Review.objects.filter(product_id=id)
            count = reviews.count()
            positive_avg = 0
            negative_avg = 0

            for i in reviews:
                positive_avg += i.positive_score
                negative_avg += i.negative_score

            # Calculate sentiment scores
            if count > 0:
                positive_avg /= count
                negative_avg /= count

            # Train a Random Forest Regressor model to predict the price optimization
            X = np.array([positive_avg, negative_avg]).reshape(1, -1)
            y = np.array([product.selling_price])
            rfr = RandomForestRegressor(n_estimators=100, random_state=42)
            rfr.fit(X, y)

            # Predict the optimized price
            optimized_price = rfr.predict([[positive_avg, negative_avg]])[0]
            if positive_avg > negative_avg:
                optimized_price *= np.random.uniform(0.95, 0.99)
            else:
                optimized_price *= np.random.uniform(1.01, 1.05)

            # Update the optimised price of the price of the product
            product.optimized_price = optimized_price
            product.save()

           # Update the sentiment table
            reviews = tbl_Review.objects.filter(product_id=id)
            count = reviews.count()
            positive_avg = 0
            negative_avg = 0
            # neutral_avg=0

            for i in reviews:
                positive_avg=positive_avg + i.positive_score
                negative_avg=negative_avg + i.negative_score
                # neutral_avg=neutral_avg + i.neutral_score
            a=positive_avg/count * 100
            b=negative_avg/count * 100
            # c=neutral_avg/count * 100
            sentiment_table=Sentiment.objects.filter(product_id=id)
            if sentiment_table:
                i=Sentiment.objects.get(product_id=id)
                i.num_reviews=count
                i.avg_pos_score=a
                i.avg_neg_score=b
                # i.avg_neu_score=c
                i.save()
            else:
                Sentiment(product_id=id, avg_pos_score=positive_avg, avg_neg_score=negative_avg, num_reviews=count).save()

            return redirect(singleproduct, product.id)
    else:
        return redirect(login)




