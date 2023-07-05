from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user-info/register', views.register, name='register'),
    path('user-info/login', views.login_view, name='login'),
    path('detail', views.detail, name='detail'),
    path('user-info', views.userInformation, name='information'),
    path('modify-password', views.modifyPassword, name='modify-password'),
    path('contact',views.contact,name='contact'),
    path('bars',views.bar_list,name='bars'),
    path('download',views.download_file,name='download'),
    path('usage',views.usage,name='usage')
]
