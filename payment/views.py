from django.shortcuts import render , redirect
from cart.cart import Cart
from django.contrib import messages
from payment.models import ShippingAddress , Order , OrderItem
from django.contrib.auth.models import User
from payment.froms import ShippingForm , PaymentForm
from store.models import Product , Profile


# Create your views here.

def orders(request , pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order_id=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                order.update(shipped=True)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request , 'Shipping status updated')
            return redirect('home')

        return render(request , 'payment/orders.html' , {'order':order , 'items':items})
    else:
        messages.success(request , 'Access denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:

        orders = Order.objects.filter(shipped=False)



        return render(request , 'payment/not_shipped_dash.html' , {'orders':orders})
    else:
        messages.success(request , 'Access denied')
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request , 'payment/shipped_dash.html' , {'orders':orders})
    else:
        messages.success(request , 'Access denied')
        return redirect('home')
    


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals_data = cart.cart_total()
        payment_form = PaymentForm(request.POST or None)


        
        #get shipping session data
        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping.get('shipping_full_name', '')
        email = my_shipping.get('shipping_email', '')   


        #create shipping address from session info
        shipping_address = f"{my_shipping.get('shipping_address1', '')}\n{my_shipping.get('shipping_address2', '')}\n{my_shipping.get('shipping_city', '')}\n{my_shipping.get('shipping_state', '')}\n{my_shipping.get('shipping_zipcode', '')}\n{my_shipping.get('shipping_country', '')}"
        amount_paid = totals_data

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user , full_name=full_name , email=email , shipping_address=shipping_address , amount_paid=amount_paid)
            create_order.save()

            #get order id 
            order_id = create_order.pk
            # get products from cart and save to order items
            for product in cart_products:
                product_id = product.id
                if product.sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id , product_id=product_id , user=user , quantity=value , price=price)
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == 'session_key' :
                    del request.session[key]

            messages.success(request , 'order placed successfully')
            return redirect('home')
       
        else:
            create_order = Order(user=None, full_name=full_name , email=email , shipping_address=shipping_address , amount_paid=amount_paid)
            create_order.save()
            #get order id 
            order_id = create_order.pk
            # get products from cart and save to order items
            for product in cart_products:
                product_id = product.id
                if product.sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id , product_id=product_id , user=None , quantity=value , price=price)
                        create_order_item.save()

            #delete the cart
            for key in list(request.session.keys()):
                if key == 'session_key' :
                    del request.session[key]

            #delete cart from old cart session database
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart='')




            messages.success(request , 'order placed successfully')
            return redirect('home')

            

        
    else:
        messages.success(request , 'Access denied')
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals_data = cart.cart_total()

        #create a session for shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request , 'payment/billing_info.html' , {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals_data,
            'shipping_info':request.POST,
            'billing_form':billing_form,
            })
        else:
            billing_form = PaymentForm()
            return render(request , 'payment/billing_info.html' , {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals_data,
            'shipping_info':request.POST,
            'billing_form':billing_form,
            })
        
        shipping_form = request.POST 
        return render(request , 'payment/billing_info.html' , {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals_data,
            'shipping_form':shipping_form,
            })
    else:
        messages.success(request , 'Access denied')
        return redirect('home')


def payment_success(request):
    return render(request , 'payment/payment_success.html')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals_data = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals_data,
        'shipping_form':shipping_form,
        })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals_data,
        'shipping_form':shipping_form,
        })

