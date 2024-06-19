from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from classes.forms import ProductForm
from classes import  forms, models
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.decorators import login_required


# Create your views here.

def HomePage(request):
    return render(request, 'home.html')
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('pass')
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            if user.is_superuser:    
                login(request, user)
                return redirect('admin_page')
            else:   
                login(request, user)
                return redirect('productPage') 
        else:
            return HttpResponse("Username or password is incorrect!") 
    return render(request, 'login.html')

def signup(reques):
    if reques.method == 'POST':
        uname = reques.POST.get('username')
        email = reques.POST.get('email')
        pass1 = reques.POST.get('password1')
        pass2 = reques.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("Password and confirm password are not same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('loginpage')
    
    return render(reques, 'signup.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                form.save(request=request)

                messages.success(request, 'Email sent with instructions to reset password')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"failed to send password reset email: {e}")
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})


def Products(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products' : products})


def AddProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added! Add another item')
            return redirect('admin_page')
    else:
        form = ProductForm()
    return render(request, 'addProduct.html', {'form': form})       #????

def logoutbutton(request):
    logout(request)
    return redirect('homepage')


def admin_page(request):
    products = Product.objects.all()
    return render(request, 'admin_page.html', {'products' : products})


def cart(request):
    prod = CartItem.objects.filter(user=request.user)
    total_pricepp = sum(item.total_price() for item in prod)

    context = {
        'cart_items' : prod,
        'total_pricepp' : total_pricepp,
    }
    return render(request, 'cart_page.html', {'prod':prod})


def add_to_cart(request):
    if request.method == 'POST':
        cart_quantity = request.POST.get("quantity")
        cart_product_id = request.POST.get("product")

        try:
            cart_product_id = int(cart_product_id)
            product = Product.objects.get(pk=cart_product_id)

            # Get all existing cart items for the user and product
            cart_items = CartItem.objects.filter(user=request.user, product=product)

            if cart_items.exists():
                # If there are existing cart items, update the first one
                cart_item = cart_items.first()
                cart_item.quantity += int(cart_quantity)
                cart_item.save()
            else:
                # If no existing cart items, create a new one
                CartItem.objects.create(
                    user=request.user,
                    product=product,
                    quantity=int(cart_quantity),
                )

            return redirect('productPage')
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)
        except MultipleObjectsReturned:
            # Handle the case where multiple cart items match the conditions
            return HttpResponse("Multiple cart items found", status=500)
    else:
        return HttpResponse(status=400)  # Bad request


def deleteProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'GET':
        product.delete()
        #Redirect to a success URL or product listpage
        return redirect('admin_page')  
    return redirect('admin_page')

    
def decrease_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_page')

def increase_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_page')


def delete_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id)
            item.delete()
            return redirect('cart_page')
        except CartItem.DoesNotExist:
            return redirect('cart_page')
    else:
        return redirect('cart_page')
    

def confirmOrder(request):
    if request.method == 'POST':
        user = request.user
        receiver_name = request.POST.get('receiver_name')
        mobile = request.POST.get('address')
        address = request.POST.get('mobile')
        payment = request.POST.get('payment')

        # Check if the user has items in the cart
        cart_items = CartItem.objects.filter(user=user)
        if cart_items.exists():
            total_amount = sum(item.total_price() for item in cart_items)
            # Create the order object
            order = Order.objects.create(user=user, receiver_name=receiver_name, address=address, mobile=mobile, payment_option=payment, total_amount = total_amount)

            # Associate the cart items with the order and save them as order items
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price)
                
            cart_items.delete()
            return redirect('cart_page')  # Redirect to a success page
        else:
            # Redirect back to the cart page with a message indicating that the cart is empty
            return redirect('cart_page')  # You can customize this redirection as per your application
    else:
        # Handle GET request for the confirmation page
        return render(request, 'cart_page.html')

def userOrder(request):
    try:
        #Fetching orders
        user_orders = Order.objects.filter(user=request.user)

        #Creating list of orders
        orders_detail = []

        for ord in user_orders:
            order_items = OrderItem.objects.filter(order=ord)
            orders_detail.append({'order': ord, 'order_items': order_items})
        
        return render(request, 'order_page_user.html', {'orders_detail': orders_detail})

    except Exception as e:
        return HttpResponse(f"An error occured: {e}")



            
# def allItems(username):
#     try:
#         # Assuming you have a User model and want to get the user object based on the username
#         user = User.objects.get(username=username)
        
#         # Retrieve cart items for the specified user
#         cart_items = CartItem.objects.filter(user=user)
        
#         # Print cart items for the user
#         for cart_item in cart_items:
#             print(cart_item)
    
#     except User.DoesNotExist:
#         print(f"User '{username}' does not exist.")

# # Call the function with the desired username
# allItems('rjt')
