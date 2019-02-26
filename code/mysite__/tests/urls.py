from django.urls import path
from .import views

app_name = 'tests' # 命名空间！
urlpatterns = [
    path('', views.index, name='index'),
    path('your_name/', views.get_name, name='get_name'),
    path('meta/', views.meta, name='meta'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login/profile/', views.profile, name='profile'),
    path('login/res/', views.my_res, name='my_res'),
    path('login/make-resvervation/', views.make_reserversion_pre, name='m_r_p'),
    path('login/make_res-t/', views.make_reserversion, name='m_r_t'),
    path('login/change_pwd/', views.change_pwd, name='change_pwd'),
]
# 终于知道这个'name'有什么用了！
# 故：在模板中使用：{% url 'app_name:name' param %}就可以映射到这个地方来！
#可算是明白了！