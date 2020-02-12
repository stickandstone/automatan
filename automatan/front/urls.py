from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='front-index'),
    path('<str:brand>/', views.brand, name='front-brand'),
    path('<str:brand>/<str:model>', views.model, name='front-model'),
    path('about/', views.about, name='front-about'),
]
