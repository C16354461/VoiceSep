from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file/<filename>/', views.file, name='file'),
    path('sep/<filename>/', views.sep, name='sep'),
]

# filename /<filename>/
