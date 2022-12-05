# C:\Users\19498\AppData\Local\Programs\Python\Python3_8\python manage.py runserver
from django.urls import path
from newssearch.views import print_page
from . import views

app_name = 'newssearch'

urlpatterns = [
    path('first_page/', print_page, name=''),
    path('', views.UserView.as_view())
]