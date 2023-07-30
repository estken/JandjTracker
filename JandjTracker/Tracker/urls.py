from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('log_complain/', views.create_log, name='log_complain')
]
