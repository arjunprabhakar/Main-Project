from django.contrib import admin
from cart.models import OrderPlaced,Payment
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,PageBreak,Spacer



# For filtering orders
import calendar
from datetime import datetime, timedelta
from django.contrib import admin
from django.db.models import Q
from datetime import datetime

from .models import Product

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Filter Product'
    parameter_name = 'ordered_date__range'

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
            return queryset.filter(ordered_date__date=today)
        elif self.value() == 'yesterday':
            yesterday = datetime.now().date() - timedelta(days=1)
            return queryset.filter(ordered_date__date=yesterday)
        elif self.value() == 'this_week':
            start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=6)
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        elif self.value() == 'last_week':
            end_date = datetime.now().date() - timedelta(days=datetime.now().weekday() + 1)
            start_date = end_date - timedelta(days=6)
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        elif self.value() == 'this_month':
            start_date = datetime(datetime.now().year, datetime.now().month, 1).date()
            end_date = start_date + timedelta(days=calendar.monthrange(datetime.now().year, datetime.now().month)[1] - 1)
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        elif self.value() == 'last_month':
            end_date = datetime(datetime.now().year, datetime.now().month, 1).date() - timedelta(days=1)
            start_date = datetime(end_date.year, end_date.month, 1).date()
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        elif self.value() == 'this_year':
            start_date = datetime(datetime.now().year, 1, 1).date()
            end_date = datetime(datetime.now().year, 12, 31).date()
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        elif self.value() == 'last_year':
            start_date = datetime(datetime.now().year - 1, 1, 1).date()
            end_date = datetime(datetime.now().year - 1, 12, 31).date()
            return queryset.filter(ordered_date__date__range=[start_date, end_date])
        return queryset




# function for generate sales report
def generate_sales_report(modeladmin, request, queryset):
    # Get the order placed objects in the queryset
    order_placed_list = list(queryset)

    # Get the payment objects associated with the order placed objects
    payment_list = Payment.objects.filter(orderplaced__in=order_placed_list)

    # Create a list of tuples with the data you want to include in the report
    report_data = []
    total_amount = 0
    serial_number = 1
    for order_placed in order_placed_list:
        payment = payment_list.filter(orderplaced=order_placed).first()
        ordered_date_str = datetime.strftime(order_placed.ordered_date, "%Y-%m-%d")
        report_data.append((serial_number, order_placed.product.name, order_placed.quantity, payment.amount,ordered_date_str))
        total_amount += payment.amount
        serial_number += 1
    # Create a PDF file with the report data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    # Create a canvas object and write the report data to it
    pdf_canvas = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Add the header
    header_style = ParagraphStyle(name="header", 
                                  fontSize=20, 
                                  textColor=colors.HexColor("#FA6803"),
                                  alignment=1,
                                  marginTop=-80,
                                  marginBottom=80)
    header = Paragraph("Smart Store", header_style)
    elements.append(header)
    elements.append(Paragraph("", header_style))
   

    elements.append(Spacer(1, 20))
    # Add the table
    data = [["Sl No","Product", "Quantity", "Amount","Order date"]]
    for serial_number,product, quantity, amount,ordered_date in report_data:
        data.append([serial_number,product, str(quantity), str(amount),ordered_date])
    total_amount_style = ParagraphStyle(name="total_amount", textColor=colors.red,fontSize=12)
    data.append(["", "","","Total Amount :",Paragraph(str(total_amount), total_amount_style)])
    table_style = TableStyle([
          ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#3D3D3D")),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor("#FFFFFF")),
    ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor("#3D3D3D")),
    ('ALIGN', (0, 1), (-1, -2), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -2), 12),
    ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
    ('GRID', (0, 0), (-1, -2), 1, colors.HexColor("#D9D9D9")),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#F2F2F2")),
    ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor("#3D3D3D")),
    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, -1), (-1, -1), 14),
    ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
    ])
    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    pdf_canvas.build(elements)

    return response
generate_sales_report.short_description = "Download sales report"




class UserAdmin(admin.ModelAdmin):
    actions = [generate_sales_report]
    verbose_name_plural = "Order Details"
    list_filter = (DateRangeFilter,)
    list_display = ('get_product_name','quantity','get_amount',)


    # for getting the product name
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'

    # for getting the payment amount
    def get_amount(self, obj):
        return obj.payment.amount
    get_amount.short_description = 'Amount'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(OrderPlaced,UserAdmin)


class PaymentAdmin(admin.ModelAdmin):


    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Payment,PaymentAdmin)


# admin.py
# admin.py

from django.http import HttpResponse
from .views import sales_report

def sales_report(request):
    return HttpResponse(sales_report(request))


