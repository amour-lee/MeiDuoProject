# 定义耗时任务
from .yuntongxun.sms import CCP
from . import constants
from celery_tasks.main import celery_app


# 使用task装饰器，将以下任务装饰为celery可以识别的异步任务
# task('send_sms_code'):给异步任务起别名，若不起，默认名字会很长
@celery_app.task('send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    定义发短信的异步任务
    :param mobile: 手机号
    :param sms_code:  短信验证码
    :return:  None
    """
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)