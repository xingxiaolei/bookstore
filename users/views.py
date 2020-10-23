from django.shortcuts import render, redirect, reverse
from users.models import Passport
import re

def register(request):
    '''注册页面'''
    return render(request, 'users/register.html')

def register_handler(request):
    '''注册页面提交表单'''

    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    #进行数据校验,三者为必填
    if not all([username, password, email]):
        return render(request, 'users/register.html', {'errmsg': '数据不能为空！'})

    #判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'users/register.html', {'errmsg': '邮箱不合法！'})

    #提交注册信息，向系统中添加账户
    try:
        Passport.objects.add_one_passport(username=username, password=password, email=email)
    except Exception as e:
        print('e:', e)
        return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})

    #注册完成，还是返回注册页
    return redirect(reverse('books:index'))

def login(request):
    '''显示登陆页面'''
    if request.COOKIES.get('username'):
        username = request.COOKIES.get('username')
        checked = 'checked'
    else:
        username = ''
        checked = ''

    context = {
        'username': username,
        'checked': checked
    }

    return render(request, 'users/login.html', context)


























































