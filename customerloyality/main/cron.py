from .models import Customer
def my_scheduled_job():
    customers=Customer.objects.all()
    for cust in customers:
            cust.total_swipes_today=0
            cust.save()