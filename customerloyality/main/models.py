from django.db import models
from django.forms import IntegerField
import datetime
# Create your models here.
class Customer(models.Model):
    driving_license=models.CharField(max_length=500,null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    EMV_num=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    total_swipes_today=models.CharField(max_length=100,null=True)
    total_swipes=models.CharField(max_length=100,null=True)
    total_redeem_rewards=models.CharField(max_length=100,null=True)
    reward_points=models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
class SwipeTime(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    time=models.DateTimeField(default=datetime.datetime.now())
    reward_points=models.IntegerField(null=True)
    def __str__(self):
        return self.customer.name
class FirstSwipeTime(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now=True)

class RewardTime(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now=True)

class RewardPoints(models.Model):
        reward_points=models.IntegerField(default=10)