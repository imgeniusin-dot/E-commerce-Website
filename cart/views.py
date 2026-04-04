from django.shortcuts import render , get_object_or_404 , redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages





# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals_data = cart.cart_total()

    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals_data,

    })

def cart_add(request):
    #get the cart 
    cart = Cart(request)

    #test for post
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))

        product_qty = int(request.POST.get('product_qty'))


        #look up product into database
        product = get_object_or_404(Product , id=product_id)
        #save to a session 
        cart.add(product=product , quantity=product_qty)

        #return resonse
        # response = JsonResponse({'Product Name': product.name})

        #get cart quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'Qty':cart_quantity})
        messages.success(request , ("Product Added to cart.. "))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))

        # call delte function to delte this 
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request , ("Product deleted  to cart.. "))
        return response




def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #get stuff
        product_id = int(request.POST.get('product_id'))

        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'Qty':product_qty})
        messages.success(request , ("Product Updated   to cart.. "))
        return response
        # return redirect('cart_summary')