from django import forms
from .models import Ticket
from django.contrib.auth import get_user_model
User = get_user_model()

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email','name','phone']
        


class TicketForm(forms.ModelForm):


    class Meta:
        model = Ticket
        fields = ['department',
        'category',
        'lab_url',
        'subject',
        'description',
        'user',
        'priority',
        'attach_file']
