from django.shortcuts import render,redirect
from django.http import HttpResponse, request, HttpResponseRedirect,JsonResponse
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def Home(request):
    customers=Customer.objects.all()
    reward_point=RewardPoints.objects.all()
    reward_point=reward_point[0].reward_points
    print(customers)
    someone_won=False
    customer_won=[]
    for customer in customers:
        if customer.reward_points==reward_point:
            someone_won=True
            customer_won.append(customer)
    context={'customers':customers,'reward_point':reward_point,'someone_won':someone_won,'customer_won':customer_won}
    return render(request,'index.html',context)

def AddNewCustomer(request):
    return render(request,'add-new-customer.html')

def AllCustomers(request):
    search = False
    q = request.args.get('q',1)
    if q:
        search = True
    print(q)
    customers=Customer.objects.paginate(int(q),20,error_out=False)
    print(customers)
    context={'customers':customers}
    return render(request,'all-customers.html',context)

# @app.route('/give-reward/<id>',methods=['POST'])
def GiveReward(id):
    name=f'id{id}'
    driving_license=request.form[name]
    print("--------------")
    print(driving_license)
    customer=Customer.objects.get(id=id)
    if str(customer.driving_licence)==str(driving_license):  
        customer.reward_points=0
        customer.total_swipes=0
        customer.total_redeem_rewards+=1
        customer.save()
        RewardTime.objects.create(
            customer=customer
        )

        # flash('Redeemed Success!')
        messages.success(request, 'Redeemed Success!.')
    else:
        # flash('error----------------')
        messages.info(request, 'Redeemed Success!.')
    print(customer)
    return redirect('/')  


# @app.route('/swipe-card/',methods=['POST'])
@csrf_exempt
def SwipeCard(request):
    # json_res=json.loads(request.POST)
    data = json.loads(request.body)
    reward_point=RewardPoints.objects.all()
    reward_point=reward_point[0].reward_points
    # print(data['emv_value
    print(data['emv_value'])
    customer = Customer.objects.filter(EMV_num = str(data['emv_value']))
    print(customer)
    if(not customer.exists()):
                    response={'success':False}
                    return JsonResponse(response)


    customer=customer[0]
    customer.total_swipes = int(customer.total_swipes) + 1 
    customer.total_swipes_today = int(customer.total_swipes_today) + 1 
    response={'success':True,'points':customer.reward_points,'swipes':customer.total_swipes_today }
    if int(customer.total_swipes_today)==1 and int(customer.total_swipes_today)<=reward_point:
        if int(customer.total_swipes)<=1:
                FirstSwipeTime.objects.create(
                                customer=customer
                            )


                customer.reward_points=str(int(customer.reward_points)+1)
                customer.save()
                SwipeTime.objects.create(
                        customer=customer,
                        reward_points=customer.reward_points
                    )

                response={'success':True,'points':customer.reward_points,'swipes':customer.total_swipes_today }
                    

    return JsonResponse(response)

# @app.route('/add-customer-api/', methods=['GET', 'POST'])
@csrf_exempt
def AddCustomerApi(request):
    data = json.loads(request.body)
    name=data['name']
    email=data['email']
    emv=data['emv']
    
    phone=data['phone']
    address=data['address']
    id_str=data['id']
    check_id=id_str[0:8]
    print(data)
    print(check_id)
    if str(emv)==str(id_str):
        messages.info(request,"ERROR: Please add customer again.")
        return JsonResponse({'success':True})
    # new_customer=Sock2(
    #         driving_licence=id_str,
    #         name=name,
    #         email=email,
    #         EMV_num=emv, 
    #         phone=phone, 
    #         address=address ,
    #         total_swipes_today=0,
    #         total_swipes=0,
    #         reward_points=0,
    #         total_redeem_rewards=0
    #     )
    # db.session.add(new_customer)
    # db.session.commit()
    Customer.objects.create(
            driving_license=id_str,
            name=name,
            email=email,
            EMV_num=emv, 
            phone=phone, 
            address=address ,
            total_swipes_today=0,
            total_swipes=0,
            reward_points=0,
            total_redeem_rewards=0   
    )
    return JsonResponse({'success':True})

# @app.route('/add_record/<to_change>', methods=['GET', 'POST'])
def AddRecord(request,to_change):
    if to_change == 'Customer':

            name = request.POST['name']
            email = request.POST['email']
            EMV_num = request.POST['EMV_num']
            phone = request.POST['phone']
            driving_licence = request.POST['driving_licence']
            address = request.POST['address']
            total_swipes_today=0
            total_swipes=0
            reward_points=0
            reward_available_to_redeem=False
            

            message = f"The data for Customer {name} has been submitted."
            return render(request,'add_record.html', message=message, to_change=to_change)
    
# app.route('/select_record/<to_change>')
# def SelectRecord(to_change):
#     if to_change == 'Image':
#         Sock = Sock1
#     elif to_change == 'Customer':
#         Sock = Sock2
#     socks = Sock.query.order_by(Sock.name).all()
#     return render_template('select_record.html', socks=socks, to_change=to_change)
@csrf_exempt
def ChangeNFC(request,customer_id):
    if request.method=='POST':
        customer=Customer.objects.get(id=customer_id)
        id=request.POST[f'id-{customer_id}']
        nfc=request.POST[f'nfc-{customer_id}']
        customer_conferm=Customer.objects.filter(driving_license=id)
        if not customer_conferm.exists():
            messages.info(request,'wrong id, please scan again')
            return redirect('/')
        if not customer_conferm[0].id==customer_id:
            messages.info(request,'wrong id, please scan again')
            return redirect('/')
        customer.EMV_num=nfc
        customer.save()
        messages.info(request,'Successfully changed!')
        return redirect('/')

    
def Dashboard(request):
    return render(request,'admin-login.html')


def GetTime(request,customer_id):
    print("--------------")
    customer=Customer.objects.get(id=customer_id)
    swipe_time=SwipeTime.objects.filter(customer=customer)
    print(swipe_time)
    response_dict={}
    for time in swipe_time:
        print(time)
        response_dict[f'{time.time.date()} , {time.time.time()}']=f'{time.reward_points}'
    response={'swipe_time':f'{swipe_time}'}
    return JsonResponse(response_dict)

def ViewTimeDashboard(request):
    
    if request.user.is_superuser:
        customers=Customer.objects.all()
        context={'customers':customers}
        return render(request,'viewadminpanell.html',context)

def RewardTimeAPI(request,customer_id):
    customer=Customer.objects.get(id=customer_id)
    reward_time=RewardTime.objects.filter(customer=customer)
    response_dict={}
    for time in reward_time:
        print(time)
        response_dict[f'{time.time.date()}']=f'{time.time.time()}'
    response={'reward_time':f'{reward_time}'}
    return JsonResponse(response_dict)



def give_reward(request,id):
    name=f'id{id}'
    driving_license=request.POST[name]
    print("--------------")
    print(driving_license)

    customer=Customer.objects.get(id=id)

    if str(customer.driving_license)==str(driving_license):  
        customer.reward_points=0
        customer.total_swipes=0
        customer.total_redeem_rewards=int(customer.total_redeem_rewards)+1
        customer.save()

        RewardTime.objects.create(
            customer=customer
        )

        messages.info(request,'Redeemed Success!')
    else:
        messages.info(request,'error..')
        

    return redirect('/') 

def report(request):
    return render(request,'report.html')
    # Make a PDF straight from HTML in a string.
    customers=Sock2.query.all()
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    html = render_template('report_template.html', customers=customers)
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"

    customers=Customer.objects.all()
    context={'customers':cuctomers}
    return render(request,'report.html',context)