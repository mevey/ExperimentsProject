from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('enroll/', views.enrollment),
    path('pre/', views.pretreatment),
    path('treat/', views.treatment),
    path('control/', views.control),
    path('post/', views.posttreatment),
]
