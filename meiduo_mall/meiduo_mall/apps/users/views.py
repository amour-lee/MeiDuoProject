from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
# Create your views here.

class MobileCountView(APIView):
    """判断手机号是否重复"""

    # url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    def get(self, request, mobile):
        """使用mobile作为条件查询满足条件的记录的数量"""
        count = User.objects.filter(mobile=mobile).count()

        # 构造响应数据
        data = {
            'mobile': mobile,
            'count': count
        }

        # 响应数据
        return Response(data)


class UsernameCountView(APIView):
    """判断用户名是否存在"""

    #  url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    def get(self, request, username):
        """使用username作为条件查询满足条件的记录的数量"""
        count = User.objects.filter(username=username).count()

        # 构造响应数据
        data = {
            'username': username,
            'count': count
        }

        # 响应数据
        return Response(data)

