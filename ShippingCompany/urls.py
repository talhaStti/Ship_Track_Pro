from django.urls import path
from . import views

urlpatterns = [
    path('', views.shippingCompanyDashboard, name="shippingCompanyDashboard"),
    path('/requestShippingCost/<int:id>', views.requestShippingCost, name="requestShippingCost"),
    path('/verifyShippingPayment/<int:id>', views.verifyPayment, name="verifyShippingPayment"),
    path('/pickTanker/<int:id>', views.pickTanker, name="pickTanker"),
    path('/dropTanker/<int:id>', views.dropTanker, name="dropTanker"),
    path('/addShippingManifest/<int:id>', views.addShippingManifest, name="addShippingManifest"),

]