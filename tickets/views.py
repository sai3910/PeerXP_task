from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Ticket
from django.core import serializers
from .forms import TicketForm, UserForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model
from .utils import upload_products_file_path, handle_uploaded_file
import json
import requests
from django.contrib.humanize.templatetags import humanize
import datetime
import os
User = get_user_model()

auth_token = os.environ['AUTH_TOKEN']
org_id=os.environ['ORG_ID']

params="sortBy=-createdTime&limit=15"

headers={
    "Authorization":auth_token,
    "orgId":org_id,
    "contentType": "application/json; charset=utf-8"
}


def addTicket(request):
    if request.method == 'GET':
        user_id = request.session['logged_User'][0]
        user_obj = User.objects.get(id=user_id)
        user_qs= User.objects.filter(id=user_id)
        form = TicketForm()
        user_form = UserForm(instance=user_obj)

        return render(request, 'add_ticket.html', {'form': TicketForm(),'user_obj': user_obj,'user_form':user_form})
    if request.method == 'POST':
        try:

            ticket_data={
                    "departmentId":"7189000000010772",#request.POST['department'],
                    

                    "contactId":"7189000000125039",#request.POST['user'],
                     
                    "subject":request.POST['subject'],
                    "email": request.POST['email'],
                    "description":request.POST['description'],
                    "priority": request.POST['priority'],
                    "category": request.POST['category'],
                    "phone": request.POST['phone']
            }
            print("ticket_data\n",ticket_data)
            # print('json.dumps(ticket_data)',json.dumps(ticket_data))
            
            post_headers={
                "Authorization":auth_token,
                "orgId":org_id,
                # "contentType": "application/json; charset=utf-8"
            }
            resp=requests.post('https://desk.zoho.in/api/v1/tickets', headers=post_headers,data=json.dumps(ticket_data))

        
            if resp.status_code == 200:
                print("Data Posted Successful,Response:")
                print(resp.content)
            else:
                print("Request not successful,Response code ",resp.status_code," \nResponse : ",resp.content)

        except:
            return redirect('add_ticket')
            pass
    return redirect('Dashboard')



def index(request):
    return render(request, 'home.html')


def userLogin(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))
            if user.check_password(request.POST.get('password')):
                if (user.is_active):
                    request.session['logged_User']=[user.id,user.email, user.name, user.phone]
                    request.user = user
                    return redirect(dashboard)
                return HttpResponse("User is inactive!!")
            return HttpResponse("Please Enter the correct Password")
        except Exception as e:
            return  HttpResponse("Exception: {}".format(e))
    return render(request, 'login.html')

def get_date(date_val):
    return humanize.naturaltime(date_val)

def dashboard(request):
    user_id = request.session['logged_User'][0]

    resp=requests.get('https://desk.zoho.in/api/v1/tickets?'+params, headers=headers)
    if resp.status_code == 200:
        print("Request Successful,Response:")
        print(resp.content)
    else:
        print("Request not successful,Response code ",resp.status_code," \nResponse : ",resp.content)
    ticket_qs = json.loads(resp.content)['data']

    # ticket_qs = Ticket.objects.filter(user_id=user_id)
    for i in ticket_qs:
        department_id = i['departmentId']
        dept_resp = requests.get('https://desk.zoho.in/api/v1/departments/'+department_id,headers=headers)
        # import pdb;pdb.set_trace()
        dept_name = json.loads(dept_resp.content)['name']

        i['departmentId'] = dept_name
    #     i['created_on'] =datetime.datetime.strptime(i['createdTime'], "%Y-%m-%dT%H:%M:%S.%fZ")

    context = {'ticket_qs':ticket_qs}
    # print(ticket_qs['data'])
    return render(request, 'dashboard.html',context)

def logout(request):
    request.session.clear()
    return redirect(index)
