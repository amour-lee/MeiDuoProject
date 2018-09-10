from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.


class SMSCodeView(APIView):
    """发送短信验证码"""

    def get(self, request, mobile):
        """
        GET /sms_codes/(?P<mobile>1[3-9]\d{9})/
        """
        pass
