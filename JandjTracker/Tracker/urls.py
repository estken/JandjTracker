from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('auth_reset_password/', views.auth_reset_password, name='auth_reset_password'),
    path('profile/', views.profile, name='profile')
]
