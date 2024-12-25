from django.urls import path
from . import views

urlpatterns = [
    path('', views.portAuthorityDashboard, name="portAuthorityDashboard"),
    path('/dispatchTanker/<int:id>', views.dispatchTanker, name="dispatchTanker"),
    

]