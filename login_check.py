
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class UserLoginMiddleware(MiddlewareMixin):
    white_list = ['/login/','/admin/','/admin/login/']  # 白名单


    def process_request(self, request):




        if not request.user.is_authenticated and request.path_info not in self.white_list and not request.path_info.startswith('/captcha'):#
            return redirect('/login/')
