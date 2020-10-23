from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),  #进入注册页面
    url(r'^register_handle/$', views.register_handler, name='register_handle'), #提交信息，添加用户
    url(r'^login/$', views.login, name='login')
]