from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='front-index'),
    path('about/', views.about, name='front-about'),
]
