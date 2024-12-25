from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name="loginView"),
    # accept post request views for signing up and logging in user
    path('login', views.loginUser, name="loginUser"),
    path('signup', views.signupUser, name="signupUser"),
    path('logout', views.logoutUser, name='logoutUser'),
]
