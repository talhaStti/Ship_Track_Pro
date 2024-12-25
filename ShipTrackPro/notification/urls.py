from django.urls import path
from . import views

urlpatterns = [
    path('', views.getNotifications, name="getNotifications"),
    path('/markAsRead/<int:id>/', views.markAsRead, name="markAsRead"),
]