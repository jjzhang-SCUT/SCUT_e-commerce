import json
from student.models import Commodities, Order
from student.models import Student
from django.http import HttpResponse, JsonResponse
from django.template import engines
from log import get_log_stu
from django.shortcuts import render


django_engine = engines['django']


def generate_order_id():
    from random import random
    return str(int(random() * 1e15))


# home/purchase?id=
def purchase_info(request):
    if get_log_stu() is None:
        return render(request, 'login.html')
    # 展示收货以及商品信息
    if request.method == 'GET':
        c_id = request.GET['id']  # 商品号
        info = Student.objects.values('name', 'dormitory', 'telephone')
        info = info.filter(student_ID=get_log_stu().student_ID)

        info2 = Commodities.objects.values('name', 'price', 'commodities_ID')
        info2 = info2.filter(commodities_ID=c_id)

        return render(request, 'purchase.html', {'info': info, 'info2': info2})

    # 确认购买，产生订单
    elif request.method == 'POST':
        id_order = generate_order_id()  # 订单号
        a = json.loads(request.body)['data']
        # print(f'a======={a}')
        c_id = json.loads(request.body)['data']['id']  # 商品号
        c = Commodities.objects.get(commodities_ID=c_id)  # 商品

        if c.inventory > 0:
            c.inventory -= 1
            c.save()
            info = json.loads(request.body)['data']
            record = Order.objects.create(order_ID=id_order,
                                          buyer_ID=get_log_stu().student_ID,
                                          consignee=info['consignee'],
                                          address=info['address'],
                                          telephone=info['telephone'],
                                          seller_ID=c.seller_ID,
                                          state=False,
                                          commodities=c)

            return JsonResponse({'ret': 0})

        elif c.inventory == 0:
            return JsonResponse({'ret': 1})
