from django.contrib.auth import authenticate

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    context = {}
    if request.method == 'POST':
        next = request.POST.get('next')
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
                    if next:
                        return redirect(next)
                    else:
                        return redirect('/')
                else:
                    context.update(msg='该用户没有激活')
                # 用户没有激活
            else:
                # 用户名密码错误
                context.update(msg='用户名密码错误')
        else:
            context.update(msg='输入信息不符合规范,请检查')
    return render(request, 'login.html', context)


def register_view(request):
    pass


def logout_view(request):
    logout(request)
    return redirect('/')
