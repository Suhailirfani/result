from django.urls import path
from . import views

app_name = 'results_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('student/result/', views.student_result_view, name='student_result'),
    path('staff/dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('staff/class/<int:class_num>/', views.class_result_view, name='class_result'),
    path('staff/class/<int:class_num>/toppers/', views.toppers_view, name='toppers'),
    path('staff/class/<int:class_num>/ranklist/', views.rank_list_view, name='rank_list'),
    path('staff/upload/single/', views.single_upload_view, name='single_upload'),
    path('staff/upload/bulk/', views.bulk_upload_view, name='bulk_upload'),
]
