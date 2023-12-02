from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/all/', views.all_products, name='listing'),
]