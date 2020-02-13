from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='front-index'),
    path('<str:brand>/', views.brand, name='front-brand'),
    path('<str:brand>/<str:model>', views.model, name='front-model'),
    path('about/', views.about, name='front-about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
