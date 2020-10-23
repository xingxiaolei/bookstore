from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
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

    #注册完成，还是返回登录页
    return redirect(reverse('user:login'))

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

def login_check(request):
    '''进行用户登陆校验'''
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remeber')

    if not all([username, password]):
        #如果有数据是空
        return JsonResponse({'res': 2})

    passport = Passport.objects.get_one_passport(username=username, password=password)

    if passport:
        next_url = reverse('books:index')
        jres = JsonResponse({'res': 1, 'next_url': next_url})

        #判断是否记住用户名
        if remember == 'true':
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            jres.delete_cookie('username')

        #记住用户的登陆状态
        request.session['is_login'] = True
        request.session['user_name'] = username
        request.session['passport_id'] = passport.id
        print(request.session.items())
        return jres
    else:
        #用户名密码错误
        return JsonResponse({'res': 0})

def logout(request):
    '''退出登录'''
    #清空用户的session信息
    request.session.flush()

    #跳转到首页
    return redirect(reverse('books:index'))



























































