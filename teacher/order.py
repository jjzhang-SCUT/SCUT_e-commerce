import json
from django.db.models import F
from log import del_log_admin, get_log_admin
from student.models import Order
from student.models import Commodities
from django.http import HttpResponse, JsonResponse
from django.template import engines
from django.shortcuts import render


django_engine = engines['django']


# admin/order
def display_order(request):
    if get_log_admin() is None:
        return render(request, 'login.html')
    # 查看所有订单
    if request.method == 'GET':
        order = Order.objects.annotate(
            commodities_ID=F('commodities__commodities_ID'),
            name=F('commodities__name'),
            price=F('commodities__price')
        ).values('order_ID',
                 'buyer_ID',
                 'seller_ID',
                 'commodities_ID',
                 'time',
                 'state',
                 'name',
                 'price')

        return render(request, 'orders.html', {'orders': order})
    # 信号量为0 退出登录
    elif request.method == 'POST':
        signal = json.loads(request.body)['signal']
        if signal == 0:
            del_log_admin()
            if get_log_admin() is None:
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1})
