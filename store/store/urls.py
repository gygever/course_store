from django.urls import path
from course_store import views

urlpatterns = [
    path('', views.index),
    path('sign_up/', views.sign_up, name='signup'),
    path('log_in/', views.log_in, name='login'),
    path('log_out/', views.log_out, name='logout'),
    path('buy_course/', views.buy_course, name='buy_course')
]
