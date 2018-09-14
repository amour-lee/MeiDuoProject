from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer
from django.conf import settings


def generate_save_user_token(openid):
    """
    使用itsdangerous对原始openid进行签名
    :param openid: 原始的openid
    :return: 签名后的openid
    """
    # 创建序列化器对象，指定秘钥和过期时间
    serializer = TJSSerializer(settings.SECRET_KEY, 300)

    # 准备原始的openid
    data = {'openid': openid}

    # 对openid进行签名,返回签名之后的bytes类型的字符串
    token = serializer.dumps(data)

    # bytes类型的字符串转成标准的字符串，并返回
    return token.decode()