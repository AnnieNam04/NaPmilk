from django.shortcuts import render
import numpy as np
import pandas as pd
import io
import os
from django.conf import settings
from store.models import Product
from analysis.utils import *
# Create your views here.
def work_with_chart_1(request):

    #barchart
    data_order_quantity = pd.read_csv(os.path.join(
        settings.MEDIA_ROOT, 'analysis/data1.csv'))
    bar_order1 = get_bar(data_order_quantity, 'order_id', 'quantity', "Orders's total quantity")

    #thống kê theo tiền
    data_order_amount = pd.read_csv(os.path.join(
        settings.MEDIA_ROOT, 'analysis/data2.csv'))
    bar_order2 = get_bar(data_order_amount, 'order_id', 'total', "Orders's total amount")
    
    #Thống kê đơn theo sản phẩm
    data_order_Product = pd.read_csv(os.path.join(
    settings.MEDIA_ROOT, 'analysis/data3.csv'))
    bar_order3 = get_bar(data_order_Product, 'product_id', 'quantity', "Orders's total quantity per Prouduct")
    
    #Thống kê đơn theo sản phẩm
   
    return render(request, "analysis/chart.html", { 'bar_order1': bar_order1,'bar_order2': bar_order2,
                                                     'bar_order3': bar_order3,})

