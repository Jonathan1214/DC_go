from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('login/', views.login, name='login'),
]