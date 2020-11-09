from django.shortcuts import render
from django.http import JsonResponse
from utils.decorators import login_required
from books.models import Books
from django_redis import get_redis_connection

#前端发过来的数据：商品id和商品数量 books_id books_count
#涉及到数据的修改使用post方式

@login_required
def cart_add(request):
    '''向购物车添加数据'''
    #接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    #进行数据校验
    if not all([books_id, books_count]):
        return JsonResponse({'res':1, 'errmsg':"数据不完整"})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})

    try:
        count = int(books_count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'商品数量必须为数字'})

    #添加商品到购物车
    #每个用户的购物车记录 用一条hash数据保存，格式： cart_用户id：商品id 商品数量
    conn = get_redis_connection('default')
    cart_key = f'cart_{request.session.get("passport_id")}'

    res = conn.hget(cart_key, books_id)
    if res is None:
        #如果用户的购物车中没有添加过该商品，则添加数据
        res = count
    else:
        # 如果用户的购物车中添加过该商品，则累计商品数量
        res = int(res)+count

    #判断商品库存
    if res > books.stock:
        return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
    else:
        conn.hset(cart_key, books_id, res)


    return JsonResponse({'res':5})

@login_required
def cart_count(request):
    '''获取用户购物车中的商品数目'''

    #计算用户购物车商品的数量
    conn = get_redis_connection('default')
    cart_key = f'cart_{request.session.get("passport_id")}'

    res = 0
    res_list = conn.hvals(cart_key)

    for i in res_list:
        res += int(i)

    return JsonResponse({'res': res})

@login_required
def cart_show(request):
    '''显示购物车页面'''
    passport_id = request.session.get('passport_id')
    #获取用户购物车的记录
    conn = get_redis_connection('default')
    cart_key = f'cart_{passport_id}'
    res_dict = conn.hgetall(cart_key)

    books_li = []
    #保存所有商品总数
    total_count = 0
    #保存所有商品的总价格
    total_price = 0

    for id,count in res_dict.items():
        #根据id获取商品信息
        books = Books.objects.get_books_by_id(books_id=id)
        #保存商品的数目
        books.count = count
        #保存商品的小计
        books.amount = int(count) * books.price
        books_li.append(books)

        total_count += int(count)
        total_price += int(count) * books.price

    context = {
        'books_li': books_li,
        'total_count': total_count,
        'total_price': total_price
    }

    print(res_dict.items())
    return render(request, 'cart/cart.html', context)

@login_required
def cart_del(request):
    '''删除用户购物车中的商品信息'''
    books_id = request.POST.get('books_id')

    if not all([books_id]):
        return JsonResponse({'res':1, 'errmsg':'数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})

    #删除购物车商品信息
    conn = get_redis_connection('default')
    cart_key = f'cart_{request.session.get("passport_id")}'
    conn.hdel(cart_key,books_id)

    return JsonResponse({'res':3})

@login_required
def cart_update(request):
    '''更新购物车数量'''

    #接收数据
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    #数据的校验
    if not all([books_id, books_count]):
        return JsonResponse({'res':1, 'errmag':'数据不完整'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})


    try:
        books_count = int(books_count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'商品数目必须为数字'})

    #更新操作
    conn = get_redis_connection('default')
    cart_key = f'cart_{request.session.get("passport_id")}'

    #判断商品库存
    if books_count > books.stock:
        return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

    conn.hset(cart_key, books_id, books_count)
    return JsonResponse({'res': 5})






































