from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/',views.check, name='login'),
    path('driversignup/', views.driverSignIn, name='driversignup'),
] 