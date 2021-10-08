from django.core.mail.message import EmailMultiAlternatives
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from app.models import Home
from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
from django.conf import settings
import datetime
import json
from products.models import Product
# Create your views here.


@login_required(login_url='signin')
def placeOrder(request, total=0):
    home = Home.objects.all()
    current_user = request.user
    cartItems = CartItem.objects.filter(user=current_user)
    cart_count = cartItems.count()
    if cart_count < 0:
        return redirect('products')
    tax = 0
    grand_total = 0
    for cartItem in cartItems:
        total += (cartItem.product.ProductPrice * cartItem.quantity)
    tax = (5*total)/100
    grand_total = total+tax
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date+str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cartItems,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'homes': home
            }
            return render(request, 'store/payments.html', context)
        else:
            return redirect('checkout')
    return redirect('cart')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])
    # store transactions
    payment = Payment.objects.create(
        user=request.user, payment_id=body['transID'], payment_method=body['payment_method'], amount_paid=order.order_total, status=body['status'])
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    # move the cart item to ordered products
    cartItems = CartItem.objects.filter(user=request.user)
    for item in cartItems:
        orderProduct = OrderProduct()
        orderProduct.order_id = order.id
        orderProduct.payment = payment
        orderProduct.user_id = request.user.id
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.color = item.itemColor
        orderProduct.size = item.itemSize
        orderProduct.product_price = item.product.ProductPrice
        orderProduct.ordered = True
        orderProduct.save()

    # # reduce the product quantity
        product = Product.objects.get(id=item.product_id)
        if product.productStock >= item.quantity:
            product.productStock -= item.quantity
        else:
            product.stock = 0
        product.save()
    # # clear the cart
    cartItems = CartItem.objects.filter(user=request.user)
    cartItems.delete()
    # send order numbers and transactions id back
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def order_complete(request):
    home = Home.objects.all()
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'homes': home
        }
        return render(request, 'store/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
