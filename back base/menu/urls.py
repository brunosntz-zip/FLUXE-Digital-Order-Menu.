from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('center-menu/', views.center_menu, name='center-menu'),
    path('detail-iten/', views.detail_iten, name='detail-iten')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
