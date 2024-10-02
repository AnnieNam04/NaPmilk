from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from . import models
from cart.forms import CartAddProductForm
import datetime
import re

# thư viện cho việc sử dụng email
from MilkStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
subcategory_list = models.SubCategory.objects.all()
subcategory = 0
search_str = ''

def index(request):
    sps = models.SubCategory.objects.filter(category=1)
    sb = models.SubCategory.objects.filter(category=2)
    product_list = models.Product.objects.order_by("-public_day")
    most_viewed_list = models.Product.objects.order_by("-viewed")[:3]
    newest = product_list[0]
    twenty_newest = product_list[:20]
    username = request.session.get('username', 0)

    return render(request, "store/index.html",
                  {'newest': newest,
                   'twenty_newest': twenty_newest,
                   'most_viewed_list': most_viewed_list,
                   'subcategories': subcategory_list,
                   'sps': sps,
                   'sb': sb,'username': username
                   })
def shop(request, pk):
    username = request.session.get('username', 0)
    subcategory = pk
    product_list = []
    subcategory_name = ''
    if pk != 0:
        product_list = models.Product.objects.filter(
            subcategory=pk).order_by("-public_day")
        selected_sub = models.SubCategory.objects.get(pk=pk)
        subcategory_name = selected_sub.name
    else:
        product_list = models.Product.objects.order_by("-public_day")

    three_newest = product_list[:3]

    page = request.GET.get('page', 1)  
    paginator = Paginator(product_list, 9)  

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "store/shop.html",
                  {'three_newest': three_newest,
                   'subcategories': subcategory_list,
                   'products': products,
                   'pk': pk,
                   'subcategories': subcategory_list,
                   'subcategory_name': subcategory_name,
                   'username': username
                   })
    
def product_detail(request, pk):
    product_select = models.Product.objects.get(pk=pk)
    models.Product.objects.filter(pk=product_select.pk).update(viewed=F('viewed') + 1)
    product_select.refresh_from_db()
    cart_product_form = CartAddProductForm()
    username = request.session.get('username', 0)

    return render(request, "store/product.html",
                {'product': product_select,
                    'subcategories': subcategory_list,
                    'cart_product_form': cart_product_form,'username': username
                    })
def cart(request):
    username = request.session.get('username', 0)
    return render(request, 'store/cart.html',
                  {'subcategories': subcategory_list,'username': username
                   })

def product(request):
    return render(request, "store/product.html")
def checkout(request):
    username = request.session.get('username', 0)
    return render(request, 'store/checkout.html',
                  {'subcategories': subcategory_list,'username': username
                   })
def contact(request):
    username = request.session.get('username', 0)
    return render(request, 'store/contact.html',
                  {'subcategories': subcategory_list,
                  'username': username})

def show_base(request):
    username = request.session.get('username', 0)

    return render(request, 'store/base.html',
                {'username': username,

                  })


def search_form(request):
    global subcategory
    global search_str
    product_items = 0
    three_newest = models.Product.objects.all().order_by("-public_day")[:3]
    product_list = []
    username = request.session.get('username', 0)

    if request.method == 'GET':
        form = forms.FormSearch(request.GET, models.Product)

        if form.is_valid():
            subcategory = form.cleaned_data['subcategory_id']
            search_str = form.cleaned_data['name']
            if subcategory != 0:
                product_list = models.Product.objects.filter(
                subcategory=subcategory, name__contains=search_str).order_by("-public_day")
            else:
                product_list = models.Product.objects.filter(
                    name__contains=search_str).order_by("-public_day")
    product_items = len(product_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 9)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "store/shop.html",
                    {'three_newest': three_newest,
                    'subcategories': subcategory_list,
                    'products': products,
                    'pk': subcategory,
                    'subcategories': subcategory_list,
                    'product_items': product_items,
                    'subcategory': subcategory,
                    'search_str': search_str, 'username': username
                    })

def sign_in(request):
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            registered = True

            #gửi email 
            email_address = form_user.cleaned_data['email']        
            subject = 'Tài khoản của Quý khách tại NaP Milk đã được tạo.'
            message = 'Hãy trải nghiệm việc mua sắm online các sản phẩm sữa tại NaP Milk.<br/> Trân trọng.'
            recepient = str(email_address)

            html_content = '<h2 style="color:blue"><i>Kính chào '+ form_user.cleaned_data['username']+',</i></h2>'\
                        + '<p>Chào mừng quý khách đến với <strong>NaP Milk</strong> website.</p>' \
                        + '<h4 style="color:red">'+ message +'</h4>'      
        
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Password và confirm password không giống nhau!')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    username = request.session.get('username', 0)
    return render(request, 'store/signin.html',
                  {'subcategories': subcategory_list,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username})

    
def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "store/login.html", {'login_result': result,
                                                        'username': username,
                                                        })
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác!"
            return render(request, "store/login.html", {'login_result': login_result})
    else:
        return render(request, "store/login.html")
@login_required
def log_out(request):
    
    logout(request)
    result = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "store/login.html", {'logout_result': result})