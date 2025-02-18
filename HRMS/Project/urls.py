from django.urls import path    
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.custom_login, name='login'),
    path('Admin_Dashboard/', views.Admin_Dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('add_department/', views.add_department, name='add_department'),
    path('update/<int:dept_id>/', views.update_department, name='update_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('departments/<int:dept_id>/', views.department_details, name='department_detail'),


    path('role_list/', views.role_list, name='role_list'),
    path('create/<int:dept_id>/', views.create_role, name='create_role'),
    path('update/<int:role_id>/', views.update_role, name='update_role'),
    path('delete/<int:role_id>/', views.delete_role, name='delete_role'),

    path('create/', views.create_employee, name='create_employee'),
    path('list/', views.employee_list, name='employee_list'),
    path('employees/update/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]
