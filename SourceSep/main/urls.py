from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file/<filename>/', views.file, name='file'),
    path('sep/<filename>/', views.sep, name='sep'),
    path('soon/', views.soon, name='soon'),
    path('samples/', views.samples, name='samples'),
]

# filename /<filename>/
