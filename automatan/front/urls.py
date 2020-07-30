from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# import django.contrib.auth.urls

urlpatterns = [
    path('', views.index, name='front-index'),
    path('about/', views.about, name='front-about'),
    path('<str:brand>/', views.brand, name='front-brand'),
    path('<str:brand>/<str:model>', views.model, name='front-model'),
    # path('users/login/', views.login_view, name='front-login')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
