from django import forms
from . import models


class FormSearch(forms.ModelForm):
    name = forms.CharField()
    subcategory_id = forms.IntegerField()

    class Meta:
        model = models.Product
        fields = ('name', 'subcategory_id')
        
class UserForm(forms.ModelForm):
    password = forms.CharField(
        max_length=150, label='Password', widget=forms.PasswordInput())
    confirm = forms.CharField(
        max_length=150, label='Confirm', widget=forms.PasswordInput())

    class Meta():
        model = models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=500, widget=forms.TextInput())
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(
        attrs={'pattern': '((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    image = forms.ImageField(required=False)

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )