import urllib

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from app.forms import RegistrationForm, LoginForm, ReviewForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, Section, Product, Order, OrderProductRelation, Review, ReviewProductRelation


def main_view(request):
    template = 'app/index.html'
    articles_data = Article.objects.all().order_by('-date_created').prefetch_related('products')
    articles = []
    for article in articles_data:
        products = []
        for product in article.products.all():
            products.append({'id': product.id, 'name': product.name, 'image': product.image, 'category': product.section.slug, 'slug': product.slug})
        articles.append({'name': article.name, 'text': article.text, 'products': products})
    context = {
        'articles': articles,
    }
    return render(request, template, context)


def signup_view(request):
    template = 'app/signup.html'
    msg = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['username']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(first_name=first_name, username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')
        else:
            form = RegistrationForm()
            msg = 'Пользователь с таким Email уже зарегистрирован либо ваши пароли не совпадают. Повторите попытку'
    else:
        form = RegistrationForm()
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, template, context)


def login_view(request):
    template = 'app/login.html'
    msg = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('main')
            else:
                form = LoginForm()
                msg = 'Данные для входа введены неправильно'
    else:
        form = LoginForm()

    context = {
        'form': form,
        'msg': msg
    }
    return render(request, template, context)


def logout_view(request):
    auth.logout(request)
    return redirect('main')


def show_section_view(request, section):
    template = 'app/smartphones.html'
    page_num = int(request.GET.get('page', 1))
    prev_page_url = None
    next_page_url = None
    pages = []

    try:
        section = Section.objects.get(slug=section)
        products = list(Product.objects.filter(section=section))
        if len(products) > 0:
            is_empty = False
            count = 6
            paginator = Paginator(products, count)
            for p in list(paginator.page_range):
                pages.append({'link': '?' + urllib.parse.urlencode({'page': p}), 'number': p})
            page_num = int(request.GET.get('page', 1))
            page = paginator.get_page(page_num)
            product_list = page.object_list
            if page.has_next():
                params = urllib.parse.urlencode({'page': page_num + 1})
                next_page_url = '?' + params
            else:
                next_page_url = None
            if page.has_previous():
                params = urllib.parse.urlencode({'page': page_num - 1})
                prev_page_url = '?' + params
            else:
                prev_page_url = None
        else:
            product_list = None
            is_empty = True
    except ObjectDoesNotExist:
        product_list = None
        is_empty = False

    context = {
        'section': section,
        'product_list': product_list,
        'is_empty': is_empty,
        'current_page': page_num,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'pages': pages
    }
    return render(request, template, context)


def show_product_view(request, section_slug, product_slug):
    template = 'app/phone.html'
    try:
        section = Section.objects.get(slug=section_slug)
        product_data = Product.objects.prefetch_related('reviews').get(section=section, slug=product_slug)

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['description']
                rating = form.cleaned_data['mark']
                author = form.cleaned_data['name']
                new_review = Review.objects.create(text=text, rating=rating, author=author, product=product_data)
                ReviewProductRelation.objects.create(product=product_data, review=new_review)
                form = ReviewForm({'name': request.user.first_name})
        else:
            form = ReviewForm({'name': request.user.first_name})
        reviews = product_data.reviews.all().order_by('-id')
        context = {
            'product_data': product_data,
            'reviews': reviews,
            'form': form
        }
    except ObjectDoesNotExist:
        context = {}

    return render(request, template, context)


def add_to_cart_view(request, product_id):
    if request.user.is_authenticated:
        this_user = request.user
        try:
            actual_order = Order.objects.get(customer=this_user, complete=False)
        except ObjectDoesNotExist:
            actual_order = Order.objects.create(customer=this_user, total=0, complete=False)
        product = Product.objects.get(id=product_id)
        try:
            product_order_relation = OrderProductRelation.objects.get(order=actual_order, product=product)
        except ObjectDoesNotExist:
            product_order_relation = OrderProductRelation.objects.create(order=actual_order, product=product, amount=0, total=0)
        product_order_relation.amount += 1
        product_order_relation.total += product.price * product_order_relation.amount
        product_order_relation.save()
        actual_order.total += product.price
        actual_order.save()

    return redirect('cart')


def show_cart_view(request):
    template = 'app/cart.html'

    if request.user.is_authenticated:
        this_user = request.user
        try:
            actual_order = Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').get(customer=this_user, complete=False)
        except ObjectDoesNotExist:
            actual_order = Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').create(customer=this_user, total=0, complete=False)

        if request.method == 'POST':
            actual_order.complete = True
            actual_order.save()
            Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').create(customer=this_user, total=0, complete=False)
            context = {
                'msg': 'Ваш заказ оформлен!'
            }

        else:
            product_order_relation = OrderProductRelation.objects.filter(order=actual_order).select_related('product')
            number_of_items = len(product_order_relation)
            items = []
            for item in product_order_relation:
                items.append({'product': item.product, 'amount': item.amount, 'total': item.total})
            context = {
                'number_of_items': number_of_items,
                'items': items,
                'total': actual_order.total,
                'order_id': actual_order.id
            }
    else:
        context = {}
    return render(request, template, context)

