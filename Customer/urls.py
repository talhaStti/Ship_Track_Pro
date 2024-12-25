from django.urls import path
from . import views

urlpatterns = [
    path('', views.customerDashboard, name="customerDashboard"),
    path('/products', views.viewProducts, name="viewProducts"),
    path('/orders', views.viewOrders, name="customerOrders"),
    path('/cart', views.viewCart, name="viewCart"),
    path('/addToCart/<int:id>', views.addToCart, name="addToCart"),
    path('/removeFromCart/<int:id>', views.removeFromCart, name="removeFromCart"),
    path('/checkout', views.checkout, name="checkout"),
    path('/orderRecieved/<int:id>', views.orderRecieved, name="orderRecieved"),


]
