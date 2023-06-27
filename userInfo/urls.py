from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-info/register', views.register, name='register'),
]
