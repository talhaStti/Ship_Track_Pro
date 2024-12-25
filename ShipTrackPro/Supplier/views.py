from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from signup.models import Supplier , OilTankerCompany , ShippingCompany , CustomAuthority
from .models import Product
from Customer.models import Order   
from django.conf import settings
import os
from openpyxl import Workbook
from notification.models import Notification





# new flow buyer places order seller accepts and requests for oil tanker filling after filling seller 
# pays custom tax then requests shipping company to pick the tanker and then shipping company drops the tanker at port 
# at the port authorities check with the custom authorities if the tax is paid before dispatching



# oil request is being sent make features acording to the flow of the programme 
# now we need to make oil tanker dashboard and make the oil filling feature and updation of excel sheet 
# then we will make request shipping company view here and then work on the shipping company dashboard
# the shipping company will further cummonicate with custom authorities and Port authorities 
# after the basic flow is done send to client for review and then make the changes and then deploy the app
# after pssing the basic flow start adding notifications for all the users
# then work on design and then finalize the application

# similar auth function will be used for all user types
def authSupplier(request):
    # print('cart' in request.session)
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'supplier':
            if Supplier.objects.filter(user=request.user).exists():
                return True
            else:
                messages.info(request, f'No Supplier with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False



def supplierDashboard(request):
    if authSupplier(request):
        wallet = Supplier.objects.get(user=request.user).wallet
        totalOrders = Order.objects.filter(product__supplier=Supplier.objects.get(user=request.user))
        completedOrders = totalOrders.filter(orderRecieved = True).count()
        ordersPending = totalOrders.count() -completedOrders
        totalProducts = Product.objects.filter(supplier=Supplier.objects.get(user=request.user)).count()

        return render(request, 'supplier/supplierDashboard.html'
                      ,{"wallet":wallet,
                        "ordersPending":ordersPending,
                        "completedOrders":completedOrders,
                        "totalProducts":totalProducts})
    else:
        return redirect('loginView')





def newProduct(request):
    if authSupplier(request):
        if request.method == 'POST':
            name = request.POST['productName']
            price = request.POST['productPrice']
            description = request.POST['productDescription']
            print(request.FILES)
            image = request.FILES['productImage']
            supplier = Supplier.objects.get(user=request.user)
            product = Product(name=name,price=price,description=description,image=image,supplier=supplier)
            product.save()
            messages.info(request, f'Product {name} added successfully')
            return redirect('supplierDashboard')
        else:
            return render(request, 'supplier/newProduct.html')
    else:
        return redirect('loginView')
    
def viewProducts(request):
    if authSupplier(request):
        products =  Product.objects.filter(supplier=Supplier.objects.get(user=request.user))
        return render(request, 'supplier/supplierProducts.html',{'products':products})
    else:
        return redirect('loginView')
    
def updateProduct(request,id):
    if authSupplier(request):
        try:
            product = Product.objects.get(id=id)
            if product.supplier.user != request.user:
                messages.info(request, f'You are not authorized to edit this product')
                return redirect('supplierProducts')
        except:
            messages.info(request, f'Product with id {id} not found')
            return redirect('supplierProducts')
        if request.method == 'POST':
            product.name = request.POST['productName']
            product.price = request.POST['productPrice']
            product.description = request.POST['productDescription']
            product.image  = request.FILES['productImage'] if 'productImage' in request.FILES else product.image

            
            product.save()
            messages.info(request, f'Product with id {product.id} has been update successfully')
            return redirect('supplierProducts')
        return render(request, 'supplier/updateProduct.html',{'product':product})
    else:
        return redirect('loginView')


def deleteProduct(request,id):
    if authSupplier(request):
        try:
            product = Product.objects.get(id=id)
            if product.supplier.user != request.user:
                messages.info(request, f'You are not authorized to delete this product')
                return redirect('supplierProducts')
            product.delete()
            messages.info(request, f'Product {product.name} deleted successfully')
        except:
            messages.info(request, f'Product with id {id} not found')
        return redirect('supplierProducts')
    else:
        return redirect('loginView')




def viewOrders(request):
    if authSupplier(request):
        orders = Order.objects.filter(product__supplier=Supplier.objects.get(user=request.user)).order_by('orderRecieved')       
        return render(request, 'supplier/supplierOrders.html',{'orders':orders})
    else:
        return redirect('loginView')


def sendOilReq(request,id):
    if authSupplier(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        if request.method == 'POST':
            orderDiagram = request.FILES['orderDiagram']
            order.diagram = orderDiagram
            order.oilReqSent = True
            order.status = "Oil Request Sent"
            fileName = f'Order_{order.id}.xlsx'
            filePath  = settings.MEDIA_ROOT + '/excelSheets/' + fileName
            workbook = Workbook()
            workbook.save(filePath)
            order.excelSheet = 'excelSheets/' + fileName
                        
            # create a excel sheet and update the oil quantity
            Notification.objects.create(user=OilTankerCompany.objects.first().user,content=f'New Order recieved for oil filling').save()
            order.save()
            messages.info(request, f'Oil Request Sent for Order {order.id}')
            return redirect('supplierOrders')
        else:
            return redirect('supplierOrders')
    else:
        return redirect('loginView')

def sendForCustomReview(request,id):
    if authSupplier(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        order.customReqSent = True
        order.status = "Waiting for custom clearance"
        order.save()
        Notification.objects.create(user=CustomAuthority.objects.first().user,content=f'New Order recieved for Custom Approval').save()
        messages.info(request, f'Order {order.id} is now waiting for customs clearance')
        return redirect('supplierOrders')
    else:
        return redirect('loginView')

def sendShipReq(request,id):
    if authSupplier(request):
        try:
            order = Order.objects.get(id=id)
        except: 
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        order.status = "Shipping Company Requested"
        order.shipReqSent = True
        order.save()
        Notification.objects.create(user=ShippingCompany.objects.first().user,content=f'New Order recieved for Shipping').save()
        messages.info(request, f'Shipping Company Requested for Order {order.id}')
        return redirect('supplierOrders')


def payCustomTax(request,id):
    if authSupplier(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        
        supplier = Supplier.objects.get(user = request.user)
        if supplier.wallet >= order.customTax:
            supplier.wallet -= order.customTax
            order.status = 'Custom Tax Paid Waiting for Conformation'
            order.customTaxSent = True
            order.save()
            supplier.save()
            Notification.objects.create(user=CustomAuthority.objects.first().user,content=f'Custom Tax recieved for order {order.id}').save()
            messages.info(request,f"Tax paid for Order {order.id} waiting for conformation")
        else:
            messages.info(request, f"Insufficeint Funds to pay Tax")
        return redirect('supplierOrders')
    else:
        return redirect('loginView')
    


    

def payShippingCost(request,id):
    if authSupplier(request):
        try:
            order = Order.objects.get(id=id)
        except:
            messages.info(request, f'Order with id {id} not found')
            return redirect('supplierOrders')
        
        supplier = Supplier.objects.get(user = request.user)
        if supplier.wallet >= order.shippingCost:
            supplier.wallet -= order.shippingCost
            order.status = 'Custom Tax Paid Waiting for Conformation'
            order.shippingCostSent = True
            order.save()
            supplier.save()
            Notification.objects.create(user=ShippingCompany.objects.first().user,content=f'Payment recieved for order {order.id}').save()
            messages.info(request,f"Shipping Cost paid for Order {order.id} waiting for conformation")
        else:
            messages.info(request, f"Insufficeint Funds to pay Shipping Cost")
        return redirect('supplierOrders')
    else:
        return redirect('loginView')



# upload document to model and assign privileges 
# shipping manifesto will be uploaded by shipping company view able by oil supplier customer and custom authorities
# oil tanker will send bills of lading
    
# vessels information and seals and containers numbers uploaded oil tanker viewable only by port authorities 

# custom documents and export declaration will be uploaded by supplier viewable only by custom authorities 

def addCustomDocumentation(request,id):
    if authSupplier(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
                if order.product.supplier.user != request.user:
                    messages.info(request, f'You are not authorized to add documents to this order')
                    return redirect('supplierOrders')
            except Order.DoesNotExist:
                print('e')
                messages.info(request, f'Order with id {id} not found')
                return redirect('supplierOrders')
            customDocumentation = request.FILES['customDocumentation']
            order.customDocumentation = customDocumentation
            order.save()
        return redirect('supplierOrders')
    else:
        return redirect('loginView')  

def addExportDeclaration(request,id):
    if authSupplier(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
                if order.product.supplier.user != request.user:
                    messages.info(request, f'You are not authorized to add documents to this order')
                    return redirect('supplierOrders')
            except:
                messages.info(request, f'Order with id {id} not found')
                return redirect('supplierOrders')
            exportDeclaration = request.FILES['exportDeclaration']
            order.exportDeclaration = exportDeclaration
            order.save()
        return redirect('supplierOrders')
    else:
        return redirect('loginView')  

