from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from signup.models import ShippingCompany
from Customer.models import Order ,ExcelSheet  
from notification.models import Notification

def authShippingCompany(request):
    # print('cart' in request.session)
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'shippingCompany':
            if ShippingCompany.objects.filter(user=request.user).exists():
                return True
            else:
                messages.info(request, f'No Oil Tanker Company with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False
    

def shippingCompanyDashboard(request):
    if authShippingCompany(request):
        orders = Order.objects.filter(oilFilled=True,shipReqSent=True,tankerDropedAtPort=False)
        return render(request, 'ShippingCompany/shippingCompanyDashboard.html',{'orders':orders})
    else:
        return redirect('loginView')
    

def pickTanker(request,id):
    if authShippingCompany(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'No Order with id {id} found')
            return redirect('shippingCompanyDashboard')
        if order.shippingCostVerified:
            order.tankerPicked = True
            order.status = "Tanker Picked"
            Notification.objects.create(user=order.product.supplier.user,content=f'Order {order.id} has been picked up by shipping company').save()
            Notification.objects.create(user=order.customer.user,content=f'Order {order.id} has been picked up by shipping company').save()
            order.save()
            messages.info(request, f'Tanker Picked for Order {order.id}')
        else: 
            messages.info(request, f'Waiting for Shipping Payment for Order {order.id}')

        return redirect('shippingCompanyDashboard')
        
    else:
        return redirect('loginView')
    
def dropTanker(request,id):
    if authShippingCompany(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'No Order with id {id} found')
            return redirect('shippingCompanyDashboard')
        if order.tankerPicked:
            order.tankerDropedAtPort = True
            order.status = "Tanker Droped At Port"
            Notification.objects.create(user=order.product.supplier.user,content=f'Order {order.id} has been Dropped at the Port').save()
            Notification.objects.create(user=order.customer.user,content=f'Order {order.id} has been Dropped at the Port').save()
            order.save()
            messages.info(request, f'Tanker Droped At Port for Order {order.id}')
        else:
            messages.info(request, f'Tanker Not Yet Picked for Order {order.id}')
        return redirect('shippingCompanyDashboard')
        
    else:
        return redirect('loginView')


def requestShippingCost(request,id):
    if authShippingCompany(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'No Order with id {id} found')
            return redirect('shippingCompanyDashboard')
        shippingCost = int(request.POST['shippingCost'])
        if shippingCost < order.product.price * 0.1:
            order.shippingCost = shippingCost
            order.status = "Shipping Cost Added"
            order.save()
            Notification.objects.create(user=order.product.supplier.user,content=f'Shipping Cost of {order.shippingCost} Added for Order {order.id}').save()
            messages.info(request, f'Shipping Cost Added for Order {order.id}')
        else:
            messages.info(request, f'Shipping Cost must be less than 10% of product price')
        return redirect('shippingCompanyDashboard')
    else:
        return redirect('loginView')
    

def verifyPayment(request,id):
    if authShippingCompany(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'No Order with id {id} found')
            return redirect('shippingCompanyDashboard')
        if order.shippingCostSent:
            order.shippingCostVerified = True
            order.status = "Shipping Cost Paid"
            order.save()
            Notification.objects.create(user=order.product.supplier.user,content=f'Shipping Cost of verified for Order {order.id}').save()
            messages.info(request, f'Shipping Cost Recieved for Order {order.id}')
        return redirect('shippingCompanyDashboard')
    else:
        return redirect('loginView')


# upload document to model and assign privileges 
# shipping manifesto will be uploaded by shipping company view able by oil supplier customer and custom authorities
    
def addShippingManifest(request,id):
    if authShippingCompany(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
            except:
                messages.info(request, f'No Order with id {id} found')
                return redirect('shippingCompanyDashboard')
            shippingManifest = request.FILES['shippingManifest']
            order.shippingManifest = shippingManifest
            order.save()
            Notification.objects.create(user=order.product.supplier.user,content=f'Shipping Manifest Added for Order {order.id}').save()
            messages.info(request, f'Shipping Manifest Uploaded for Order {order.id}')
        return redirect('shippingCompanyDashboard')
    else:
        return redirect('loginView')
    


