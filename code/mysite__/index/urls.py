from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('show_img/', views.show_img, name='show_img'),
    path('uploading/', views.uploading, name='uploading')
    # path('')
]