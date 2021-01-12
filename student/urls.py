from django.urls import path
from student.homepage import display_commodities
from student.sales import display_sales
from student.profile import display_profile
from student.order import display_order
from student.purchase import purchase_info
from student.detail import display_detail

urlpatterns = [
    path('', display_commodities, name='home'),
    path('sales/', display_sales, name='home/sales'),
    path('profile/', display_profile, name='home/profile'),
    path('order/', display_order, name='home/order'),
    path('purchase/', purchase_info, name='home/purchase'),
    path('detail/', display_detail, name='home/detail')
]
