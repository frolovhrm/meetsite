from django.urls import path
from meetplan.views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', meet, name='meet'),
    path('room/', room, name='room'),
    path('param/', param, name='param'),
    path('plan/', plan, name='plan')

]