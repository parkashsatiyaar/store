from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from cart.models import CartItem
from cart.views import _getCartId
from orders.models import OrderProduct
from products.models import Product, ProductGallery, ReviewRating
from .models import Banner, Category, Home
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
import random
# Create your views here.


def error_404(request, exception):
    home = Home.objects.all()
    context = {
        'homes': home,
    }
    return render(request, 'store/404.html', context)


def error_500(request, *args, **kwargs):
    home = Home.objects.all()
    context = {
        'homes': home,
    }
    return render(request, 'store/500.html', context)


def index(request):
    products = Product.objects.filter(
        is_available=True)
    products = list(products)
    random.shuffle(products)
    products = products[:20]
    home = Home.objects.all()
    banner = Banner.objects.all()
    context = {
        'products': products,
        'homes': home,
        'banners': banner,
    }
    return render(request, "store/index.html", context)


def category(request, category=None):
    products = []
    categories = Category.objects.all()
    cat = Category.objects.filter(catSlug=category).first()
    if cat:
        products = Product.objects.filter(
            productCategory=cat.id, is_available=True)
        paginator = Paginator(products, 21)
        page = request.GET.get("page")
        pagedProduct = paginator.get_page(page)
        home = Home.objects.all()
        context = {
            'products': pagedProduct,
            'homes': home,
            'categories': categories,
        }
    else:
        return redirect('products')
    return render(request, "store/products.html", context)


def products(request):
    home = Home.objects.all()
    categories = Category.objects.all()
    if "searchKeyword" in request.GET:
        keyword = request.GET.get("searchKeyword")
        products = Product.objects.order_by(
            "-created_date").filter(Q(is_available=True) & Q(Q(productDescription__icontains=keyword) | Q(productTitle__icontains=keyword) | Q(productName__icontains=keyword) | Q(ProductPrice__icontains=keyword) | Q(productKeyword__icontains=keyword)))
    else:
        products = Product.objects.all().filter(is_available=True)
        products = list(products)
        random.shuffle(products)
    paginator = Paginator(products, 21)
    page = request.GET.get("page")
    pagedProduct = paginator.get_page(page)
    context = {
        'products': pagedProduct,
        'homes': home,
        'categories': categories,
    }
    return render(request, "store/products.html", context)


def singleProduct(request, name):
    product = Product.objects.filter(
        is_available=True, productSlug=name)
    productGallery = ProductGallery.objects.filter(product__productSlug=name)
    singleProduct = Product.objects.get(
        is_available=True, productSlug=name)
    if product:
        products = Product.objects.filter(
            is_available=True)
        products = list(products)
        random.shuffle(products)
        products = products[:20]
    else:
        return redirect('products')
    inCart = CartItem.objects.filter(cart__cartId=_getCartId(
        request), product=singleProduct).exists()
    try:
        orderProduct = OrderProduct.objects.filter(
            user=request.user, product_id=singleProduct.id).exists()
    except:
        orderProduct = None
    reviews = ReviewRating.objects.filter(
        product_id=singleProduct.id, status=True)[:10]
    context = {
        'products': products,
        'singleProduct': product,
        'inCart': inCart,
        'productGallery': productGallery,
        'orderProduct': orderProduct,
        'reviews': reviews,
    }
    return render(request, "store/product.html", context)


def contact(request):
    home = Home.objects.all()
    context = {
        'homes': home,
    }
    return render(request, "store/contact.html", context)


def about(request):
    home = Home.objects.all()
    context = {
        'homes': home,
    }

    return render(request, "store/about.html", context)


@login_required(login_url='signin')
def submit_review(request, product_id):
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(
                user=request.user, product=product_id)
            review.subject = request.POST['subject']
            review.review = request.POST['review']
            review.rating = request.POST['rating']
            review.save()
        except:
            review = ReviewRating()
            review.subject = request.POST['subject']
            review.review = request.POST['review']
            review.rating = request.POST['rating']
            review.ip = request.META.get('REMOTE_ADDR')
            review.product_id = product_id
            review.user_id = request.user.id
            review.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
