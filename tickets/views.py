from django.http import JsonResponse
from django.shortcuts import render
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
User = get_user_model()



# def dashboard_with_pivot(request):
#     return render(request, 'dashboard_with_pivot.html', {})

# def pivot_data(request):
#     dataset = Order.objects.all()
#     data = serializers.serialize('json', dataset)
#     return JsonResponse(data, safe=False)

def addTicket(request):
    if request.method == 'GET':
        user_id = request.session['logged_User'][0]
        user_obj = User.objects.get(id=user_id)
        user_qs= User.objects.filter(id=user_id)
        form = TicketForm()
        user_form = UserForm(instance=user_obj)

        return render(request, 'add_ticket.html', {'form': TicketForm(),'user_obj': user_obj,'user_form':user_form})
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['attach_file'])
            form.user= request.session['logged_User'][2];
            form.save()
            return redirect(dashboard)
        # print(form.errors)
        # print(form.non_field_errors)
    return render(request, 'add_ticket.html', {'form': TicketForm()})


# def sendEmail(request):
#     print("preparing to send mail")
#     name="Sambit Kumar Sahoo"
#     domain="http://weown.properties"
#     body="http://weown.properties"
#     body = loader.render_to_string('email.html', {'name':name,'domain':domain,'body':body})
#     send_mail(
#         subject = 'Weown Properties',
#         message='',
#         html_message = body,
#         from_email = settings.EMAIL_HOST_USER,
#         recipient_list = ['dj@yopmail.com','paridadibyajyoti4@gmail.com','sambitsahoo.sks@gmail.com'],
#         fail_silently = False,
#     )
#     return HttpResponse("hii, Mail sent!!")

def index(request):
    return render(request, 'home.html')


# def userRegistration(request):
#     if request.method=='POST':
#         user = User(
#             username = request.POST.get('username'),
#             first_name = request.POST.get('first_name'),
#             last_name = request.POST.get('last_name'),
#             email = request.POST.get('email')
#         )
#         user.set_password(request.POST.get('password'))
#         user.is_active = True
#         user.save()
#         return redirect(index)
#     return render(request, 'registration.html')

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

def dashboard(request):
    # print(request.user.email)
    user_id = request.session['logged_User'][0]
    ticket_qs = Ticket.objects.filter(user_id=user_id)
    context = {'ticket_qs':ticket_qs}
    # import pdb;pdb.set_trace()
    return render(request, 'dashboard.html',context)

def logout(request):
    request.session.clear()
    return redirect(index)
