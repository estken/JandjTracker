from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('log_complain/', views.create_log, name='log_complain'),
    path('auth_login/', views.auth_login, name='auth_login'),
    path('auth_reset_password/', views.auth_reset_password, name='auth_reset_password'),
    path('profile/', views.profile, name='profile'),
    path('profile/profile_details', views.profile_details, name="profile_details"),
    path('logout/', views.log_out, name='logout'),
    path('pending_complains/', views.pending_complains, name='pending_complains'),
    path('review_complains/<int:pk>', views.review_complains, name='review_complains'),
    path('review_complains/detail_review_complains/<int:id>', views.detail_review_complains, name='detail_review_complains'),
    path('client_delete/<int:id>', views.client_delete, name='client_delete'),
    path('all_complains/', views.all_complains, name='all_complains'),
    path('activities/', views.activities, name='activities'),
    path('view_activity/<int:id>', views.view_activity, name='view_activity'),
    path('del_activities/<int:id>', views.del_activities, name='del_activities'),
    path('edit_complain/<int:pk>/edit', views.edit_complains, name='edit_complain'),
    path('pend_jobs/', views.pend_jobs, name='pend_jobs'),
    path('view_details/<int:pk>', views.view_details, name='view_details'),
    path('pend_payments', views.pend_payments, name='pend_payments'),
    path('complete_jobs/', views.complete_jobs, name='complete_jobs'),
    path('pending_jobs_link/', views.pending_jobs_link, name='pending_jobs_link'),
    path('approve_all_pend_job/<int:pk>/approve', views.approve_all_pend_job, name='approve_all_pend_job'),
    path('all_pending_payment/', views.all_pending_payment, name='all_pending_payment'),
    path('approve_all_payments/<int:pk>/approve', views.approve_all_payments, name='approve_all_payments'),
    path('completed_payments/', views.completed_payments, name='completed_payments'),

]
