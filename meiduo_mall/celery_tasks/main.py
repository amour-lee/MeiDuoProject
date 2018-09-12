# celery 启动的入口：# 创建celery对象，加载celery配置,注册celery任务
from celery import Celery


# 创建celery对象, 别名'meiduo'，celery名字，没有实际意义
celery_app = Celery('meiduo')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])