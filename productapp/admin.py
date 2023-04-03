import calendar
from datetime import datetime, timedelta
import admin_thumbnails
import csv
from django.contrib import admin
from django.http import HttpResponse

# Register your models here.
from .models import Product, Productgallery, Sentiment, tbl_Review

# def export_users(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="Users.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Name','Description','selling_price','Stock','Product Added On'])
#     Product = queryset.values_list('name', 'description','selling_price','stock','created')
#     for user in Product:
#         writer.writerow(user)
#     return response
# export_users.short_description = 'Download Product Details'




from django.contrib import admin
from django.db.models import Q
from datetime import datetime

from .models import Product

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Filter Product'
    parameter_name = 'created__range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('this_week', 'This week'),
            ('last_week', 'Last week'),
            ('this_month', 'This month'),
            ('last_month', 'Last month'),
            # ('custom', 'Custom range'),
             ('this_year', 'This year'),
            ('last_year', 'Last year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            today = datetime.now().date()
            return queryset.filter(created__date=today)
        elif self.value() == 'yesterday':
            yesterday = datetime.now().date() - timedelta(days=1)
            return queryset.filter(created__date=yesterday)
        elif self.value() == 'this_week':
            start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=6)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_week':
            end_date = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)
            start_date = end_date - timedelta(days=6)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'this_month':
            start_date = datetime(datetime.now().year, datetime.now().month, 1).date()
            end_date = start_date + timedelta(days=calendar.monthrange(datetime.now().year, datetime.now().month)[1] - 1)
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_month':
            end_date = datetime(datetime.now().year, datetime.now().month, 1).date() - timedelta(days=1)
            start_date = datetime(end_date.year, end_date.month, 1).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'this_year':
            start_date = datetime(datetime.now().year, 1, 1).date()
            end_date = datetime(datetime.now().year, 12, 31).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        elif self.value() == 'last_year':
            start_date = datetime(datetime.now().year - 1, 1, 1).date()
            end_date = datetime(datetime.now().year - 1, 12, 31).date()
            return queryset.filter(created__date__range=[start_date, end_date])
        return queryset


#Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=Productgallery
    extra=1


# from django.utils.html import format_html
# class ProductAdmin(admin.ModelAdmin):
#     list_editable=['selling_price','stock']
#     prepoluted_fields={'slug':('name',)}
#     list_per_page=20
#     actions = [export_users]
#     exclude = ('percentage',)
#     list_display=['image_tag','name','stock','selling_price']
#     inlines=[ProductGalleryInline]
#     list_filter = (DateRangeFilter,)
#     def image_tag(self, obj):
#         return format_html('<img src="{}" height="50"/>'.format(obj.image.url))

#     image_tag.short_description = 'Image'
    
#     # For Calculating Product Percentage   
#     def save_model(self, request, obj, form, change):
#         percentage =obj.percentage
#         percentage=100-((obj.selling_price/obj.original_price)*100)
#         obj.percentage=percentage
#         super().save_model(request, obj, form, change)
#     class Media:
#         css = {
#             'all': ('/static/custome.css', ),
#         }
# admin.site.register(Product,ProductAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display=['product','review','rating','date']
#     # def has_add_permission(self, request, obj=None):
#     #     return False

#     # def has_change_permission(self, request, obj=None):
#     #     return False
# # ddd
#     # def has_delete_permission(self, request, obj=None):
#     #     return False
#     verbose_name_plural = "Product Reviews"
# admin.site.register(tbl_Review,UserAdmin)




from django.contrib import admin
from django.db.models import Avg
from textblob import TextBlob
from .models import Product, tbl_Review
from django.db.models import Avg
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import urllib
from django.utils.html import format_html


class ReviewInline(admin.TabularInline):

    def has_add_permission(self, request, obj=None):
        return False
    can_delete = False
    model = tbl_Review
    extra = 0
    fields = ('review', 'rating', 'positive_sentiment_score', 'negative_sentiment_score', 'neutral_sentiment_score',)
    readonly_fields = ('review', 'rating', 'positive_sentiment_score', 'negative_sentiment_score', 'neutral_sentiment_score',)
    
    def get_sentiment_score(self, instance):
        blob = TextBlob(instance.review)
        return round(blob.sentiment.polarity, 2)
    
    def positive_sentiment_score(self, instance):
        sentiment_score = self.get_sentiment_score(instance)
        if sentiment_score > 0.2:
            return sentiment_score
        return None
    
    def negative_sentiment_score(self, instance):
        sentiment_score = self.get_sentiment_score(instance)
        if sentiment_score < -0.2:
            return sentiment_score
        return None
    
    def neutral_sentiment_score(self, instance):
        sentiment_score = self.get_sentiment_score(instance)
        if sentiment_score >= -0.2 and sentiment_score <= 0.2:
            sentiment_score=0.5
            return sentiment_score
        return None

    

    
    positive_sentiment_score.short_description = 'Positive Sentiment Score'
    negative_sentiment_score.short_description = 'Negative Sentiment Score'
    neutral_sentiment_score.short_description = 'Neutral Sentiment Score'
   
    

class SentimentInline(admin.TabularInline):
    verbose_name = 'Sentiment Analysy'
    def has_add_permission(self, request, obj=None):
        return False
    model=Sentiment
    extra=0
    can_delete = False
    fields = ('sentiment_graph',)
    readonly_fields = ('sentiment_graph',)

    def sentiment_graph(self, obj):
        avg_pos_score = obj.avg_pos_score
        avg_neg_score = obj.avg_neg_score
        avg_neu_score = obj.avg_neu_score

        # create a bar plot with positive and negative scores
        fig, ax = plt.subplots()
        ax.bar(['Positive', 'Negative','Neutral'], [avg_pos_score, avg_neg_score, avg_neu_score], color=['red', 'blue','green'])
        # ax.hist([positive_score, negative_score], bins=10, color=['green', 'red'])
        # set the title and labels
        ax.set_title('Sentiment Analysis')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Average Score')

        # save the plot to a buffer
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        import base64

        # encode the buffer as base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        from django.utils.safestring import mark_safe
        # return the HTML template with the encoded image
        return mark_safe('<img src="data:image/png;base64,{}" />'.format(image_base64))




class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductGalleryInline,ReviewInline,SentimentInline]
    list_display = ('image_tag','name', 'category', 'subcategory', 'stock', 'available','selling_price',)
    list_editable=['selling_price','stock']
    search_fields = ('name', 'description')
    list_per_page=5
    exclude = ('percentage','sentiment_score',)
    list_filter = (DateRangeFilter,)

    def sentiment_score(self, obj):
        reviews = tbl_Review.objects.filter(product=obj)
        if reviews:
            sentiment_scores = []
            for review in reviews:
                blob = TextBlob(review.review)
                sentiment_scores.append(blob.sentiment.polarity)
            average_score = sum(sentiment_scores) / len(sentiment_scores)
            return round(average_score, 2)
        return None
    sentiment_score.short_description = 'Sentiment Score'
    def image_tag(self, obj):
        return format_html('<img src="{}" height="50"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'
    
    # For Calculating Product Percentage   
    def save_model(self, request, obj, form, change):
        percentage =obj.percentage
        percentage=100-((obj.selling_price/obj.original_price)*100)
        obj.percentage=percentage
        super().save_model(request, obj, form, change)
    class Media:
        css = {
            'all': ('/static/custome.css', ),
        }
    def sentiment_score_avg(self, obj):
        reviews = tbl_Review.objects.filter(product=obj)
        return reviews.aggregate(Avg('rating'))['rating__avg']
    sentiment_score_avg.short_description = 'Sentiment Score (Avg)'
    
admin.site.register(Product, ProductAdmin)


