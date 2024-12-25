from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from signup.models import PortAuthority
from Customer.models import Order   
from notification.models import Notification


def authPortAuthority(request):
    # print('cart' in request.session)
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'portAuthority':
            if PortAuthority.objects.filter(user=request.user).exists():
                return True
            else:
                messages.info(request, f'No Oil Tanker Company with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False
    

def portAuthorityDashboard(request):
    if authPortAuthority(request):
        orders = Order.objects.filter(tankerDropedAtPort=True,tankerDispatched = False)
        return render(request, 'PortAuthority/portAuthorityDashboard.html',{'orders':orders})
    else:
        return redirect('loginView')
    

def dispatchTanker(request,id):
    if authPortAuthority(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'No Order with id {id} found')
            return redirect('portAuthorityDashboard')
        # check if custom tax is paid
        if not order.tankerDropedAtPort:
            messages.info(request, f'Order {order.id} has not reached the port yet')
            return redirect('portAuthorityDashboard')

        if order.customCleared:
            order.tankerDispatched = True
            messages.info(request, f'Order {order.id} Dispatched Successfully!!')
            Notification.objects.create(user=order.product.supplier.user,content=f'Order {order.id} Dispatched successfully').save()

            order.status = 'Order Dispatched'
        else:
            messages.info(request, f'Custom Verification required before Dispatching {order.id}')
            Notification.objects.create(user=order.product.supplier.user,content=f'Order {order.id} is currently awaiting customs clearance at the port').save()
            order.status = 'Custom Verification Required'
        order.save()
        return redirect('portAuthorityDashboard')
    else:
        return redirect('loginView')