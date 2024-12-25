from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from signup.models import CustomAuthority
from Customer.models import Order   
from notification.models import Notification


def authCustomAuthority(request):
    # print('cart' in request.session)
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'customAuthority':
            if CustomAuthority.objects.filter(user=request.user).exists():
                return True
            else:
                messages.info(request, f'No Oil Tanker Company with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False
    

def customAuthorityDashboard(request):
    if authCustomAuthority(request):
        orders = Order.objects.filter(customReqSent=True,customCleared =False)
        return render(request, 'CustomAuthority/CustomAuthorityDashboard.html',{'orders':orders})
    else:
        return redirect('loginView')
    
def addCustomTax(request,id):
    if authCustomAuthority(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
            except:
                messages.info(request, f'No Order with id {id} found')
                return redirect('customAuthorityDashboard')
            tax = int(request.POST['tax'])
            if tax < order.product.price * 0.05:
                order.customTax = tax
                order.status = "Awaiting Tax Payment"
                order.save()
                messages.info(request, f'Tax Added for Order {order.id}')
                Notification.objects.create(user=order.product.supplier.user,content=f'Custom Tax of {order.customTax} Added for Order {order.id}').save()
            else:
                messages.info(request, f'Tax must be less than 5% of product price')
            return redirect('customAuthorityDashboard')
        else:
            return redirect('customAuthorityDashboard')
    else:
        return redirect('loginView')

def verifyPayment(request,id):
    if authCustomAuthority(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        if order.customTaxSent:
            if not order.customDocumentation:
                Notification.objects.create(user=order.product.supplier.user,content=f'Awaiting Custom Documentation for Order {order.id}').save()
                messages.info(request, f'Custom Documentation missing for Order {order.id}')
                return redirect('customAuthorityDashboard')
            if not order.exportDeclaration:
                Notification.objects.create(user=order.product.supplier.user,content=f'Awaiting Export Declaration documents for Order {order.id}').save()
                messages.info(request, f'Export Declaration Document missing for Order {order.id}')
                return redirect('customAuthorityDashboard')

            order.customCleared = True
            order.status = "Custom Cleared"
            order.save()
            messages.info(request, f'Custom Cleared for Order {order.id}')
            Notification.objects.create(user=order.product.supplier.user,content=f'Customs Cleared for Order with Id {order.id}').save()

        else:
            messages.info(request, f'Tax not Recieved for order {order.id}')

        return redirect('customAuthorityDashboard')
    else:
        return redirect('loginView')
