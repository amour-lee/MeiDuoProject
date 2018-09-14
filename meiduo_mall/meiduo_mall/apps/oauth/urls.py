from django.conf.urls import url
from . import views



urlpatterns = [
    # 获取QQ登录扫码页面
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # 处理QQ扫码登录回调
    url(r'^qq/user/$', views.QQAuthUserView.as_view()),
]