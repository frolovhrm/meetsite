"""
URL configuration for meetsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from meetplan import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('my_form/', views.my_form, name='my_form'),
    path('modelform/', views.model_form, name='modelform'),
    path('userform/', views.user_form, name='userform'),
    path('setappform/', views.setapp, name='setapp'),
    path('listofprof/', views.listofprof, name='listofprof'),
    path('param/', views.param, name='param'),
    path('meet/', views.meet, name='meet'),
    path('room/', views.room, name='room'),
    path('plan/', views.plan, name='plan')

]
