from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from signup.models import Customer
from Supplier.models import Product
from .models import Order
from notification.models import Notification


# similar auth function will be used for all user types
def authCustomer(request):
    print('cart' in request.session)
    if request.user.is_authenticated:
        print(request.session.get('userType',None))
        print(request.user.username)
        if request.session.get('userType',None) == 'customer':
            if Customer.objects.filter(user=request.user).exists():
                if 'cart' not in request.session:
                    print("resetting cart")
                    request.session['cart'] = []
                return True
            else:
                messages.info(request, f'No Customer with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False



def customerDashboard(request):
    print("here")
    if authCustomer(request):
        customer = Customer.objects.get(user=request.user)
        totalOrders = Order.objects.filter(customer = customer)
        completedOrders = totalOrders.filter(orderRecieved = True).count()
        totalOrders = totalOrders.count()
        itemsInCart = len(request.session['cart'])
        return render(request, 'customer/customerDashboard.html',
                      {"customer":customer,
                        "totalOrders":totalOrders,
                        "completedOrders":completedOrders,
                        "itemsInCart":itemsInCart})
    else:
        return redirect('loginView')

   
def viewProducts(request):
    if authCustomer(request):
        print(request.session['cart'],"printing cart in viewProducts")
        products = Product.objects.all()
        return render(request, 'customer/customerProducts.html',{'products':products})
    else:
        return redirect('loginView')
    


# return with all the products using ids in session['cart']
# use this template to ask for credit card info etc and then show payment successfull page 
def viewCart(request):
    if authCustomer(request):
        total = 0
        products = []
        for  id in request.session['cart']:
            try:
                total += Product.objects.get(id=id).price
                products.append(Product.objects.get(id=id))
                # products = [Product.objects.get(id=id) for id in request.session['cart']]
            except Product.DoesNotExist:
                messages.info(request, f'No Product with id {id} found')  
                request.session['cart'].remove(id)  
                request.session.modified = True  
                return redirect('viewProducts')
        return render(request, 'customer/customerCart.html',{'products':products,'total':total})
    else:
        return redirect('loginView')



# add remove based on product id  
def addToCart(request,id):
    if authCustomer(request):
        try:
            Product.objects.get(id=id)
        except:
            messages.info(request, f'No Product with id {id} found')    
            return redirect('viewProducts')
        request.session['cart'].append(id)
        print(request.session['cart'],"printing cart")
        request.session.modified = True
        messages.info(request, f'Product added to cart')
        return redirect('viewProducts')
    else:
        return redirect('loginView')
    


def removeFromCart(request,id):
    if authCustomer(request):
        try:
            Product.objects.get(id=id)
        except:
            messages.info(request, f'No Product with id {id} found')    
            return redirect('viewCart')
        if id in request.session['cart']:
            request.session['cart'].remove(id)
            request.session.modified = True
            messages.info(request, f'Product removed from cart')
        return redirect('viewCart')
    else:
        return redirect('loginView')



# validate credit card number display success page and request.session['cart'] = []  if valid  else redirect to cart page with message
    
# add validation for credit card number and pin in template and here
def checkout(request):
    if authCustomer(request):
        total =  0
        for  id in request.session['cart']:
            try:
                total += Product.objects.get(id=id).price
                # products = [Product.objects.get(id=id) for id in request.session['cart']]
            except Product.DoesNotExist:
                messages.info(request, f'No Product with id {id} found')  
                request.session['cart'].remove(id)  
                request.session.modified = True  
        if request.method == 'POST':
            creditCardNumber = request.POST['creditCardNumber']
            pin = request.POST['pin']
            address = request.POST['address']
            print(creditCardNumber,pin,address)
            for id in request.session['cart']:
                product = Product.objects.get(id=id)
                order = Order.objects.create(customer=Customer.objects.get(user=request.user),address=address,total=total,product=product)
                Notification.objects.create(user=product.supplier.user,content=f'New Order of Product {product.name} recieved').save()
                order.save()
                supllier = product.supplier
                supllier.wallet += product.price
                supllier.save()
                
            request.session['cart'] = []    
            messages.info(request, f'Order Placed Successfully!')
            return redirect('customerDashboard')
        else:
            return render(request, 'customer/checkout.html',{'total' : total})
    else:
        return redirect('loginView')
    
# def payment(request):
#     if authCustomer(request):
#         return render(request, 'customer/payment.html')
#     else:
#         return redirect('loginView')
    



def viewOrders(request):
    if authCustomer(request):
        orders = Order.objects.filter(customer=Customer.objects.get(user=request.user)).order_by('orderRecieved')
        return render(request, 'customer/customerOrders.html',{'orders':orders})
    else:
        return redirect('loginView')




# def trackOrder(request):
#     if authCustomer(request):
#         return render(request, 'customer/trackOrder.html')
#     else:
#         return redirect('loginView')



def orderRecieved(request,id):
    if authCustomer(request):
        print("in orderRecieved")
        try:
            order = Order.objects.get(id=id)
            if order.customer.user != request.user:
                messages.info(request, f'You are not authorized to view this page')
                return redirect('customerOrders')
            order.orderRecieved = True
            order.status = "Order Recieved"
            messages.info(request, f'Order with id {id} recieved')
            order.save()
            Notification.objects.create(user=order.product.supplier.user,content=f'Order {order.id} was recieved by customer').save()
        except Order.DoesNotExist:
            messages.info(request, f'No Order with id {id} found')

        return redirect('customerOrders')
    else:
        return redirect('loginView')


