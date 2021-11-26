"""PuYuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('auth/', views.login_request),
    path('auth/logout/',views.logout_request),
    path('verification/send/', views.send),
    path('verification/check/<str:token>',views.check),
    path('password/forgot/',views.password_forgot),
    path('password/reset/',views.reset_password),
    path('register/check/',views.register_check),
    path('user/',views.user_set),
    path('user/default/',views.user_default),
    path('user/setting/',views.userdata),
    path('notification/', views.notification),
    path('user/a1c/', views.ShowHbA1c),
    path('user/medical/', views.Medical_information),
    path('user/drug-used/',views.drug),
    path('user/badge/',views.badge),
    path('news/', views.newnews),
    path('share/', views.share),                       #串完
    path('share/<int:relation_type>', views.share_check),
]
