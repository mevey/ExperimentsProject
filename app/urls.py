from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('enroll/', views.enrollment),
    path('pre/', views.pretreatment),
    path('treat/', views.treatment),
    path('number-check/', views.number_check),
    path('control/', views.control),
    path('post/', views.posttreatment),
    path('final/', views.final),
    path('download/', views.download),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
