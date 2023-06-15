from django.contrib import admin
from django.urls import path,include
from . import views
#for each functions at views.py

app_name = 'imgUpload'

urlpatterns = [
    path('', views.home, name='home'),  #if some one reaches this pg
    path('imageprocess/',views.imageprocess, name='imageprocess'),
]
