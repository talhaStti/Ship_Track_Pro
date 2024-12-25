from django.urls import path
from . import views

urlpatterns = [
    path('', views.oilTankerDashboard, name="oilTankerDashboard"),
    path('/completeOrder/<int:id>', views.completeOrder, name="completeFilling"),
        path('/addBillsOfLading/<int:id>', views.addBillsOfLading, name="addBillsOfLading"),
        path('/addVesselInformation/<int:id>', views.addVesselInformation, name="addVesselInformation"),
        path('/addSealContainerNumber/<int:id>', views.addSealContainerNumber, name="addSealContainerNumber"),
        path('/excelSheet/<int:id>', views.excelSheet, name="excelSheet"),
        path('/downloadExcelSheet/<int:id>', views.downloadExcelSheet, name="downloadExcelSheet"),

]