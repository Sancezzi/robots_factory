from django.urls import path

from .views import create_robot_view

app_name = 'robots'

urlpatterns = [
    path('create_robot/',  create_robot_view, name='create_robot'),
]