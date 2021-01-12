from log import get_log_admin
from student.models import Commodities, Comment
from django.template import engines
from django.shortcuts import render


django_engine = engines['django']


def display_detail(request):
    if get_log_admin() is None:
        return render(request, 'login.html')
    c_id = request.GET['id']
    commodities = Commodities.objects.values('commodities_ID',
                                             'seller_ID',
                                             'name',
                                             'price',
                                             'inventory',
                                             'description')
    commodities = commodities.filter(commodities_ID=str(c_id))

    comments = Comment.objects.values('comment')
    comments = comments.filter(commodities_ID=str(c_id))

    return render(request, 'admin_detail.html', {'commodities': commodities, 'comments': comments})
