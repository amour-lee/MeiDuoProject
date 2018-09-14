from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
import logging
from .models import OAuthQQUser
from .utils import generate_save_user_token
# Create your views here.


# 日志记录器
logger = logging.getLogger('django')

# url(r'^qq/user/$', views.QQAuthUserView.as_view()),
class QQAuthUserView(APIView):
    """处理QQ扫码登录的回调：完成oauth2.0认证过程"""

    def get(self, request):
        # 提取code请求参数
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建oauthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            open_id = oauth.get_open_id(access_token)

        except Exception as e:
            logger.info(e)
            return Response({'message': 'QQ服务器内部错误'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 使用openid查询该QQ用户是否在美多商城中绑定过用户
        try:
            oauthqquser_model = OAuthQQUser.objects.get(openid=open_id)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没绑定美多商城用户，创建用户并绑定到openid
            # 为了方便后续使用openid去绑定美多商城用户，现在需要将openid响应给用户
            # return Response({'openid':open_id}) # 不能将openid以明文的形式发送出去，需要混淆，让外界不知道原始数据
            openid_access_token = generate_save_user_token(open_id)
            return Response({'access_token': openid_access_token})

        else:
            # 如果openid已绑定美多商城用户，直接生成JWT token，并返回，user_id,username,token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取oauth_user关联的user
            # user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
            user = oauthqquser_model.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({
                'user_id': user.id,
                'username': user.username,
                'token': token
            })



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