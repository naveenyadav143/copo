from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_cos/', views.add_cos, name='add_cos'),
    path('add_pos/', views.add_pos, name='add_pos'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/po_attainment/', views.calculate_po_attainment, name='po_attainment'),
    path('courses/<int:course_id>/enter_matrix/', views.enter_matrix, name='enter_matrix'),
]