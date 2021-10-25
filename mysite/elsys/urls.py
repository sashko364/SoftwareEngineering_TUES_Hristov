from django.urls import include, path
from elsys import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('about', views.about),
    path('cars', views.cars),
]
