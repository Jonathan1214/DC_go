from django.urls import path
from .import views

app_name = 'tests' # 命名空间！
# path('', views.index, name='index'),
urlpatterns = [
    path('', views.index, name='index'),
    # path('your_name/', views.get_name, name='get_name'),
    path('meta/', views.meta, name='meta'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('staff_profile/', views.stf_profile, name='stf_profile'),
    path('staff/query/', views.query_result, name='query_result'),

    path('res/', views.my_res, name='my_res'),
    path('make-resvervation/', views.make_reserversion_pre, name='m_r_p'),
    path('make_res-t/', views.make_reserversion, name='m_r_t'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),
    path('contact/', views.contact, name='contact'),
    path('register', views.register, name='register')
]
# 终于知道这个'name'有什么用了！
# 故：在模板中使用：{% url 'app_name:name' param %}就可以映射到这个地方来！
#可算是明白了！

# 这边还可以配置图像路径？