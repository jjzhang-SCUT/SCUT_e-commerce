import json
from student.models import Order
from student.models import Commodities, Comment
from django.http import JsonResponse
from django.template import engines
from log import get_log_stu
from django.shortcuts import render
from django.db.models import F

django_engine = engines['django']


# home/order
def display_order(request):
    if get_log_stu() is None:
        return render(request, 'login.html')
    # 展示所有订单
    if request.method == 'GET':
        # 信号量为1:买家订单 信号量为2:卖家订单
        v = request.GET['view']
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
        if v == "buyer":
            order = order.filter(buyer_ID=str(get_log_stu().student_ID))
        elif v == "seller":
            order = order.filter(seller_ID=str(get_log_stu().student_ID))

        return render(request, 'order.html', {'order': order, 'view': v})

    # 确认收货 需要信号量0
    elif request.method == 'POST':
        comment = json.loads(request.body)['data']['comment']
        id_order = json.loads(request.body)['data']['id']  # 订单编号
        signal = json.loads(request.body)['data']['signal']
        if signal == 0:
            o = Order.objects.get(order_ID=id_order)
            Comment.objects.create(buyers_ID=get_log_stu().student_ID,
                                   commodities_ID=o.commodities.commodities_ID,
                                   comment=comment)
            o.state = True
            o.save()
            if o.state:
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1})
