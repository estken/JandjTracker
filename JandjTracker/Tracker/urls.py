from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('log_complain/', views.create_log, name='log_complain'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('auth_reset_password/', views.auth_reset_password, name='auth_reset_password'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.log_out, name='logout'),

]
