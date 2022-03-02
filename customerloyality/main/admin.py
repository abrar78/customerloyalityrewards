from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(RewardPoints)
admin.site.register(SwipeTime)
admin.site.register(FirstSwipeTime)
admin.site.register(RewardTime)

class CustomerAdmin(admin.ModelAdmin):
    
    search_fields = ['name', 'email' ]
    
admin.site.register(Customer,CustomerAdmin)