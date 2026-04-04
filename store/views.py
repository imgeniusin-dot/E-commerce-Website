from django.shortcuts import render , redirect
from .models import Product , Category , Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .froms import SignUpForm , UpdateUserForm , ChangePassword , UserInfo


from payment.froms import ShippingForm
from payment.models import ShippingAddress




from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.
def category_summary(request):
    categories = Category.objects.all()
    return render(request , 'category_summary.html' , {"categories":categories})   


def category(request , foo):
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request , 'category.html' , {'products':products , 'category':category})
    except:
        messages.success(request , ("Woops !! this Category doesn't exits"))
        return redirect('home')



def product(request , pk):
    product = Product.objects.get(id=pk)
    return render(request , 'product.html' , {'product':product})


def home(request):
    products = Product.objects.all()
    return render(request , 'home.html' , {'products':products})

def about(request):
    return render(request , 'about.html' , {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)

            #adding cart persistance
            current_user = Profile.objects.get(user__id=request.user.id)

            save_cart = current_user.old_cart

            if save_cart:
                converted_cart =json.loads(save_cart)


                cart = Cart(request)

                for key , value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)





            messages.success(request , ("you have been logged in ('-') " ))
            return redirect('home')
        else:
            messages.success(request , ("Something wet wrong try again ! "))
            return redirect('login')
        
    else:
        return render(request , 'login.html' , {})

def logout_user(request):
    logout(request)
    messages.success(request , ("You have been log out "))
    return redirect('home')

def regiter_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user 
            user = authenticate(username=username , password=password)
            login(request , user)
            messages.success(request , ("Congrates you have create an account Now Fill The Below Info "))
            return redirect('update_info')
        else:
            messages.success(request , ("Woops !! there is something went wrong try again  "))
            return redirect('register')

    else:
        return render(request , 'register.html' , {'form':form})
    

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None , instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request , ("User Update profile succes !  "))
            return redirect('update_user')
        return render(request , 'update_user.html' , {'user_form':user_form})
    else:
        messages.success(request , ("You have to been looged in to acces to page  !  "))
        return redirect(request , 'home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)

        # FIX: unpack tuple correctly
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        # shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfo(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your User Info has been updated successfully!")
            return redirect('update_user')

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "You need to be logged in to access this page!")
        return redirect('home')

    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePassword(current_user , request.POST)
            if form.is_valid():
                form.save()
                messages.success(request , ("Your Password has been Updated.."))
                login(request , current_user)
                return redirect('update_user')
            else:
                for field_errors in form.errors.values():
                    for error in field_errors:
                        messages.error(request, error)
                return render(request , 'update_password.html' , {'form':form})

        else:
            form = ChangePassword(current_user)
            return render(request , 'update_password.html' , {'form':form})
    else:
        messages.success(request , ("You have to been looged in to acces to page  !  "))   
        return redirect(request , 'home') 
    

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # i stands for insensitive
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(descrption__icontains=searched))

        if not searched:
            messages.success(request , "Sorry ! That Product doen't Exits ")
            return render(request , 'search.html' ,{})
        else:
            return render(request , 'search.html' ,{'searched':searched})
    else:
        return render(request , 'search.html' ,{})