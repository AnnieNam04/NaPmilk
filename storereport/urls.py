from django.urls import path
from . import views

app_name = 'storereport'

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.my_report, name='my_report'),
    path('easypdf', views. html_to_pdf_view),
]
