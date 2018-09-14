from django.shortcuts import render
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from rest_framework.response import Response
# Create your views here.


# url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """返回QQ扫码登录连接"""
    def get(self, request):

        # 获取next参数：
        # http://127.0.0.1:8080/login.html?next=user_center_info.html
        # http://127.0.0.1:8080/login.html
        # QQ登录成功后进入next
        next = request.query_params.get('next')
        if not next:
            next = '/'  # QQ登录结束后进入主页


        # 创建OAuthQQ对象
        # oauth = OAuthQQ(client_id='101474184', client_secret='c6ce949e04e12ecc909ae6a8b09b637c', redirect_uri='http://www.meiduo.site:8080/oauth_callback.html', state=next)
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET, redirect_uri=settings.QQ_REDIRECT_URI, state=next)

        # 调用 获取扫码链接的的方法
        login_url = oauth.get_qq_url()

        # 将扫码链接响应给浏览器
        return Response({'login_url':login_url})