import os

from django.shortcuts import render, redirect

from .models import UserInfo, UserBar
from .register import UserRegistrationForm
from .login import UserLoginForm
from django.http import JsonResponse, FileResponse, HttpResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature
from .modify_password import ModifyUserPassword
from .user_suggest import UserSuggestForm
from django.conf import settings

# 创建令牌生成器
serializer = URLSafeTimedSerializer('wyf')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # 返回成功的 JSON 响应
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # 返回失败的 JSON 响应和表单错误信息
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            user_name = form.cleaned_data.get('username')
            token = serializer.dumps({'user_id': user_id, 'username': user_name})
            return JsonResponse({'success': True, 'token': token})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('token')  # 获取请求中的 token（假设存储在 Cookie 中）

        if not token:
            # 如果没有 token，用户未登录，重定向到登录页面或其他适当的处理方式
            return redirect('login')  # 登录页面的URL名称

        try:
            # 创建反序列化器，使用与生成 token 相同的密钥
            data = serializer.loads(token)  # 解析 token

            user_id = data.get('user_id')
            username = data.get('username')
            if user_id is None or username is None:
                return redirect('login')  # 登录页面的URL名称

            # 将 user_id 和 username 添加到 kwargs 中，传递给视图函数
            # kwargs['user_id'] = user_id
            kwargs['username'] = username

        except BadSignature:
            # token 无效，用户未登录，重定向到登录页面或其他适当的处理方式
            return redirect('login')  # 登录页面的URL名称

        return view_func(request, *args, **kwargs)

    return wrapper


def detail(request):
    return render(request, 'detail.html')


@login_required
def modifyPassword(request, username):
    if request.method == 'POST':
        form = ModifyUserPassword(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            print(errors)
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ModifyUserPassword()
    return render(request, 'modify_password.html', {'form': form})


@login_required
def userInformation(request, username):
    return render(request, 'information.html')


@login_required
def contact(request, username):
    if request.method == 'POST':
        form = UserSuggestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # 重定向到成功页面
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserSuggestForm()
    return render(request, 'contact.html', {'form': form})


@login_required
def bar_list(request, username):
    bars = UserBar.objects.filter(username=username)
    return render(request, 'bars.html', {'bars': bars})


def download_file(request):
    file_name = request.GET.get('file_name')
    # 获取要下载的文件路径
    file_path = os.path.join(settings.BASE_DIR, 'userInfo', 'static', 'soft', file_name)

    # 打开文件并创建文件响应
    try:
        # 打开文件并创建文件响应
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    except FileNotFoundError:
        return HttpResponse('<h1 style="color:red;">File not found.</h1>')

def usage(request):
    return render(request,'usage.html')