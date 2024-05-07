from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("registration/", views.registerPage, name="registration"),
    path("varify/<str:users>/", views.varify, name="varify"),
    path("logout/", views.logout, name="logout"),
]
