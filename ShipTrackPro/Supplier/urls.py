from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplierDashboard, name="supplierDashboard"),
    path('/orders', views.viewOrders, name="supplierOrders"),
    path('/product', views.viewProducts, name="supplierProducts"),
    path('/newproduct', views.newProduct, name="newProduct"),
    path('/deleteproduct/<int:id>', views.deleteProduct, name="deleteProduct"),
    path('/sendOilReq/<int:id>', views.sendOilReq, name="sendOilReq"),
    path('/sendShipReq/<int:id>', views.sendShipReq, name="sendShipReq"),
    path('/sendForCustomReview/<int:id>', views.sendForCustomReview, name="sendForCustomReview"),
    path('/payCustomTax/<int:id>', views.payCustomTax, name="payCustomTax"),
    path('/payShippingCost/<int:id>', views.payShippingCost, name="payShippingCost"),
    path('/updateProduct/<int:id>', views.updateProduct, name='updateProduct'),
    path('/addCustomDocumentation/<int:id>', views.addCustomDocumentation, name='addCustomDocumentation'),
    path('/addExportDeclaration/<int:id>', views.addExportDeclaration, name='addExportDeclaration'),
    
    

]
