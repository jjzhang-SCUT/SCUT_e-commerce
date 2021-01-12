import json
import os

from student.models import Commodities
from student.models import Student
from django.http import HttpResponse, JsonResponse
from django.template import engines
from log import get_log_stu
from django.shortcuts import render
from CEC.settings import STATICFILES_DIRS


django_engine = engines['django']


def generate_commodity_id():
    from random import random
    return str(int(random() * 1e8))


# /home/sales
def display_sales(request):
    if get_log_stu() is None:
        return render(request, 'login.html')

    # 展示在卖商品
    if request.method == 'GET':
        commodities = Commodities.objects.values('commodities_ID', 'name', 'price', 'description',
                                                 'inventory')
        commodities = commodities.filter(seller_ID=str(get_log_stu().student_ID), state=False)
        commodities = reversed(commodities)
        if 'adding' in request.GET and request.GET['adding'] == 'true':
            return render(request, 'sales.html', {'commodities': commodities, 'adding': 'true'})
        return render(request, 'sales.html', {'commodities': commodities, 'adding': 'false'})

    # 无信号量:新增售卖商品
    # 有信号量:删除商品
    elif request.method == 'POST':
        if not request.POST.get('signal'):
            commodity_id = generate_commodity_id()
            info = request.POST
            record = Commodities.objects.create(commodities_ID=commodity_id,
                                                seller_ID=get_log_stu().student_ID,
                                                name=info['name'],
                                                price=info['price'],
                                                description=info['description'],
                                                inventory=info['inventory'],
                                                state=False)
            if request.FILES.get('file'):
                file = request.FILES.get('file')
                with open(os.path.join(STATICFILES_DIRS[0], f'picture/{commodity_id}.jpg'), 'wb') as f:
                    for line in file.chunks():
                        f.write(line)
        else:
            c_id = request.POST.get('id')  # 商品id
            c = Commodities.objects.get(commodities_ID=c_id)
            c.state = True
            c.save()

        commodities = Commodities.objects.values('commodities_ID', 'name', 'price', 'description',
                                                 'inventory')
        commodities = commodities.filter(seller_ID=str(get_log_stu().student_ID), state=False)
        commodities = reversed(commodities)
        return render(request, 'sales.html', {'commodities': commodities})
