from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = "home"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_course',views.add_course,name='add_course'),
    path('courses', views.courses, name='courses'),  # Fixed typo: was 'couses'
    path('add_co',views.add_co, name='add_co'),
    path('add_po',views.add_po, name='add_po'),
    path('add_mapping/', views.add_mapping, name='add_mapping'),
    path('upload-marks/', views.upload_marks, name='upload_marks'),
    path('co-attainment/', views.co_attainment_view, name='co_attainment'),
    path('po-attainment/', views.calculate_po_attainment, name='po_attainment'),
    path("guide/", views.guide, name="guide"),
]
