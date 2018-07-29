from django.contrib.auth import authenticate

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username and password:
            # 不判断激活状态
            user = authenticate(username=username, password=password)
            if user:
                # 0 表示没有激活  1 表示激活状态  -1   表示用户删除
                if user.is_active:
                    # 记录用户登录状态
                    login(request, user)
                    return redirect('/')
                else:
                    pass
                # 用户没有激活
            else:
                # 用户名密码错误
                pass
        else:
            pass
    return render(request, 'login.html')


def register_view(request):
    pass


def logout(request):
    pass
