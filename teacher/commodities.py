import json
from student.models import Commodities
from django.http import HttpResponse, JsonResponse
from log import del_log_admin, get_log_admin
from django.template import engines
from django.shortcuts import render


django_engine = engines['django']


# admin/commodities
def display_commodities(request):
    if get_log_admin() is None:
        return render(request, 'login.html')
    # 展示商品
    if request.method == 'GET':
        commodities = Commodities.objects.values()
        commodities = commodities.filter(state=False)
        return render(request, 'commodity.html', {'commodities': commodities})

    # 删除商品->信号量为1  退出登录->信号量为0
    elif request.method == 'POST':
        signal = json.loads(request.body)['signal']
        if signal == 1:
            c_id = json.loads(request.body)['id']  # 商品id
            c = Commodities.objects.get(commodities_ID=c_id)
            c.state = True
            c.save()
            return JsonResponse({'ret': 0})
        elif signal == 0:
            del_log_admin()
            if get_log_admin() is None:
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1})
