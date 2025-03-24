from django.contrib import admin
from django.urls import path, include
from myApp import views
import myApp

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logOut/', views.logOut, name='logOut'),
    path('registry/', views.registry, name='registry'),
    path('salaryChar/', views.salaryChar, name='salaryChar'),
    path('educationChar/', views.educationChar, name='educationChar'),
    path('cityChar/', views.cityChar, name='cityChar'),
    path('dataChar/', views.dataChar, name='dataChar'),
    path('Usercenter/', views.Usercenter, name='Usercenter'),
    # path('likedata/', views.likedata, name='likedata'),
    path('cloudeChar/', views.cloudeChar, name='cloudeChar'),
    path('recommend/', views.recommend, name='recommend'),
    path('dp_page/', views.dp_page, name='dp_page'),
    path('chat_with_deepseek/', views.chat_with_deepseek, name='chat_with_deepseek'),
    path('api/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/favorites/', views.get_favorites, name='get_favorites'),

]
