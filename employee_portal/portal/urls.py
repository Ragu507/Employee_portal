from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home page
    path('', views.home, name='home'),

    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/status/', views.update_task_status, name='update_task_status'),

    # Leave URLs
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/create/', views.leave_create, name='leave_create'),
    path('leaves/<int:leave_id>/update/', views.update_leave, name='update_leave'),
    path('leaves/<int:leave_id>/delete/', views.delete_leave, name='delete_leave'),
    path('leaves/<int:leave_id>/status/', views.update_leave_status, name='update_leave_status'),

    # Salary URLs
    path('salaries/', views.salary_list, name='salary_list'),
    path('salaries/create/', views.salary_create, name='salary_create'),
    path('salaries/<int:salary_id>/update/', views.update_salary, name='update_salary'),
    path('salaries/<int:salary_id>/delete/', views.delete_salary, name='delete_salary'),
    path('salaries/<int:salary_id>/download_payslip/', views.download_payslip, name='download_payslip'),

    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark_read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
