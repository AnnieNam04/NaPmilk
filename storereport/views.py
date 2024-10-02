from django.shortcuts import render
from django.http import HttpResponse
# from reportlab.pdfgen import canva
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from store import models
from orders.models import Order, OrderItem
from django.db.models import Count,Sum, F, Value, FloatField
import pdfkit
import os
from datetime import date

def html_to_pdf_view(request):
    path_wkthtmlopdf = b'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf = path_wkthtmlopdf)
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    product_list = models.Product.objects.values('subcategory', 'name').annotate(
        total =Count('subcategory')).order_by('subcategory')
    html_string = render_to_string(
        'storereport/easyreport.html', {'product':product_list, 'day': d})
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', 'report.pdf'), configuration = config)
    html = "<html><body>" + html_string+"<h3>Thống kê đã được lưu vào tập tin report.pdf trong thư mục Document.</h3></body></html>"
    return HttpResponse(html)

def my_report(request):
    return render(request, "storereport/my_report.html")