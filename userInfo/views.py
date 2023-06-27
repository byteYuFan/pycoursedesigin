from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .register import UserRegistrationForm
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # 保存新用户记录
            return redirect('home')  # 注册成功后重定向到成功页面
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')
