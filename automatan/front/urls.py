from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TestList
# import django.contrib.auth.urls

urlpatterns = [
    path('test/', TestList.as_view()),
    path('', views.index, name='front-index'),
    path('about/', views.about, name='front-about'),
    path('<str:brand>/', views.brand, name='front-brand'),
    path('<str:brand>/<str:model>', views.year, name='front-year-page'),
    path('<str:brand>/<str:model>/<str:year>/',
         views.model, name='front-model'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
