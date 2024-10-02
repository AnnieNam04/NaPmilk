from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to="store/images", default="store/images/default.png")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="store/images", 
                              default="store/images/default.png")
    content = RichTextUploadingField(blank=True, null=True)
    public_day = models.DateTimeField(default=datetime.datetime.now)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "store/images/", default="store/images/people_default.png")    
    
    def __str__(self):
        return self.user.username 