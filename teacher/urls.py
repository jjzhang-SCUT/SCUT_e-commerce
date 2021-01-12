from django.urls import path
from teacher.commodities import display_commodities
from teacher.order import display_order
from teacher.profile import display_profile
from teacher.detail import display_detail

urlpatterns = [
    path('commodities/', display_commodities, name='admin/commodities'),
    path('order/', display_order, name='admin/order'),
    path('detail/', display_detail, name='admin/detail/'),
]
