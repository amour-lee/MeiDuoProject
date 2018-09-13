from django.contrib.auth.backends import ModelBackend
from .models import User
import re



def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 可以是用户名，也可以是手机号
    :return: user/None
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username = account)
    except User.DoesNotExist:
        return None
    else:
        return user





class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证方式"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """根据username(此时不仅仅表示用户名，主要是账号，可以是用户名也可以是手机号)
        :param request: 本次登录请求
        :param username: 可以是用户名也可以是手机号
        :param password: 密码明文
        :param kwargs: 额外参数
        :return: user
        """
        # 使用账号或者手机号查询用户
        user = get_user_by_account(username)

        # 如果用户存在，就校验密码，密码正确就返回user
        if user and user.check_password(password):
            return user