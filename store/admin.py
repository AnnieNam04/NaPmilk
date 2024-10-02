from django.contrib import admin
import datetime
# Register your models here.
from .models import Category, SubCategory, Product, UserProfileInfo

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(UserProfileInfo)
#Changing title of Django Admin
admin.site.site_header = "NaP Milk Admin"



    
