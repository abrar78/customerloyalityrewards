from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('', Home),
     path('add-customer/', AddNewCustomer),
     path('swipe-card/', SwipeCard),
     path('add-customer-api/', AddCustomerApi),
     path('customer/change-nfc/<str:customer_id>', ChangeNFC),
     path('dashboard/', Dashboard),
     path('get/<int:customer_id>/time', GetTime),
     path('view-time/', ViewTimeDashboard),
     path('get/<str:customer_id>/time-reward/',RewardTimeAPI),
     path('give-reward/<str:id>',give_reward),
     path('report/',report),
]
