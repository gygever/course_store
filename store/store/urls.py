from django.urls import path
from course_store import views

urlpatterns = [
    path('', views.index),
    path('sign_up', views.sign_up)
]
