from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from signup.models import OilTankerCompany
from Customer.models import Order ,ExcelSheet  
from notification.models import Notification
import csv
from django.http import HttpResponse



def authOilTanker(request):
    # print('cart' in request.session)
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'oilTanker':
            if OilTankerCompany.objects.filter(user=request.user).exists():
                return True
            else:
                messages.info(request, f'No Oil Tanker Company with username {request.user.username} found')
                logout(request)
                request.session['userType'] = None 
        else:
            messages.info(request, 'You are not authorized to view this page')
        return False
    

def oilTankerDashboard(request):
    if authOilTanker(request):
        orders = Order.objects.filter(oilReqSent=True,oilFilled=False)
        return render(request, 'OilTanker/oilTankerDashboard.html',{'orders':orders})
    else:
        return redirect('loginView')



# also we will create a download excel file view in here and authenticate supplier and oil tanker and then convert over model to a csv file and send it to the user
def downloadExcelSheet(request,id):
    try:
        order = Order.objects.get(id=id)
    except:
        messages.info(request, f'No Order with id {id} found')
        return redirect('loginView')
    try:
        excelSheet = ExcelSheet.objects.get(order=order)
    except:
        excelSheet = ExcelSheet.objects.create(order=order)
        excelSheet.save()
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'shippingCompany' or request.session.get('userType',None) == 'oilTanker': 
            data  = dict()
            data = {
            'volume'  : excelSheet.volume,
            'toGoMt'  : excelSheet.toGoMt,
            'rate'  : excelSheet.rate,
            'tankPressure'  : excelSheet.tankPressure,
            'weight'  : excelSheet.weight,
            }
            print(data.keys())
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{order.id}.csv"'

            csv_header = data.keys()

            csv_writer = csv.DictWriter(response, fieldnames=csv_header)
            csv_writer.writeheader()

            csv_writer.writerow(data)
            return response

    else:
        return redirect('loginView')


# this link will change to accept post and get requests get request wll show the page and post will update excel sheet
def excelSheet(request,id):
    try:
        order = Order.objects.get(id=id)
    except:
        messages.info(request, f'No Order with id {id} found')
        return redirect('loginView')
    try:
        excelSheet = ExcelSheet.objects.get(order=order)
    except:
        excelSheet = ExcelSheet.objects.create(order=order)
        excelSheet.save()
    oilTanker = False
    if request.user.is_authenticated:
        if request.session.get('userType',None) == 'supplier': 
            return render(request, 'OilTanker/updateExcelSheet.html',{
                'excelSheet':excelSheet,
                'oilTanker':oilTanker,
            })

    if authOilTanker(request):
        oilTanker = True
        if request.method == 'POST':
            print('post Request recieved')
            excelSheet.volume = request.POST['volume']
            excelSheet.toGoMt = request.POST['toGo']
            excelSheet.rate = request.POST['rate']
            excelSheet.tankPressure = request.POST['tankPressure']
            excelSheet.weight = request.POST['weight']
            excelSheet.save()


            messages.info(request, f'Excel Sheet Updated for Order {order.id}')
            Notification.objects.create(user=order.product.supplier.user,content=f'Excel Sheet for Order {order.id} was updated').save()
            return redirect('oilTankerDashboard')
        else:
            return render(request, 'OilTanker/updateExcelSheet.html',{
                'excelSheet':excelSheet,
                'oilTanker':oilTanker,
            })
    else:
        return redirect('loginView')

def completeOrder(request,id):
    if authOilTanker(request):
        order = Order.objects.get(id=id)
        if order.vesselInformation and order.sealContainerNumber and order.billsOfLading:
            order.oilFilled = True
            order.shipReqSent = True
            order.status = "Oil Filled"
            order.save()
            messages.info(request, f'Oil Filled for Order {order.id}')
            Notification.objects.create(user=order.product.supplier.user,content=f'Oil has been filled for Order {order.id}').save()

        else:
            messages.info(request, f'Vessel Information, Seal Container Number and Bills Of Lading are required to complete the order')
        return redirect('oilTankerDashboard')
        
    else:
        return redirect('loginView')




def addBillsOfLading(request,id):
    if authOilTanker(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
            except:
                messages.info(request, f'No Order with id {id} found')
                return redirect('oilTankerDashboard')
            order.billsOfLading = request.FILES['billsOfLading']
            order.save()
            messages.info(request, f'Bills Of Lading Added for Order {order.id}')
            Notification.objects.create(user=order.product.supplier.user,content=f'Bills Of Lading has been added for order {order.id}').save()
        return redirect('oilTankerDashboard')
        
    else:
        return redirect('loginView')




def addVesselInformation(request,id):
    if authOilTanker(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
            except:
                messages.info(request, f'No Order with id {id} found')
                return redirect('oilTankerDashboard')
            order.vesselInformation = request.FILES['vesselInformation']
            order.save()
            messages.info(request, f'Vessel Information Added for Order {order.id}')
            # Notification.objects.create(user=order.product.supplier.user,content=f'Vessel information has been added for order {order.id}').save()
        return redirect('oilTankerDashboard')
        
    else:
        return redirect('loginView')
    
def addSealContainerNumber(request,id):
    if authOilTanker(request):
        if request.method == 'POST':
            try:
                order = Order.objects.get(id=id)
            except:
                messages.info(request, f'No Order with id {id} found')
                return redirect('oilTankerDashboard')
            order.sealContainerNumber = request.FILES['sealContainerNumber']
            order.save()
            messages.info(request, f'Seal Container Number Added for Order {order.id}')
        return redirect('oilTankerDashboard')
        
    else:
        return redirect('loginView')
    


