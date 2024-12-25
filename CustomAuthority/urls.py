from django.urls import path
from . import views

urlpatterns = [
    path('', views.customAuthorityDashboard, name="customAuthorityDashboard"),
    path('/addCustomTax/<int:id>', views.addCustomTax, name="addCustomTax"),
    path('/verifyPayment/<int:id>', views.verifyPayment, name="verifyTaxPayment"),
]