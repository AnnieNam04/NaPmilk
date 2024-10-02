from django.urls import path
from . import views

app_name ='analysis'

urlpatterns = [
    path('chart', views.work_with_chart_1)
]
