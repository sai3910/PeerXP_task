from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .managers import UserManager
from django.contrib.humanize.templatetags import humanize


class User(AbstractUser):
	email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
	name = models.CharField(max_length=30, blank=True, null=True)
	phone = models.CharField(max_length=30, blank=True,  null=True)
	
	username = None
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
	objects = UserManager()
	
	# def __str__(self):
	# 	return self.name


class Department(models.Model):
	name = models.CharField(max_length=30,null=True,blank=False)
	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=30,null=True,blank=False)
	department = models.ForeignKey(Department,related_name= "categ_dept",on_delete=models.PROTECT)
	def __str__(self):
		return self.name

class Ticket(models.Model):
	PRIOTITY_CHOICES = (
		('High', 'HIGH - Production System Down'),
		('Med', 'MED - System Impaired'),
		('Low', 'LOW - General Guidence'),
	)
	lab_url = models.URLField(null=True,blank=False)
	department = models.ForeignKey(Department,related_name= "ticket_dept",on_delete=models.PROTECT)
	category = models.ForeignKey(Category,related_name= "ticket_categ",on_delete=models.PROTECT)
	subject = models.CharField(max_length=150,null=True,blank=False)
	user = models.ForeignKey(User,related_name= "ticekt_user",on_delete=models.PROTECT)
	description =  models.TextField(null=True,blank=True)
	priority = models.CharField(max_length=30,choices=PRIOTITY_CHOICES,null=True)
	created_on = models.DateTimeField(auto_now=True,blank=True)
	attach_file = models.FileField(_('Data File'),upload_to='attachment_records', null=True)

	def get_date(self):
		return humanize.naturaltime(self.created_on)
		
	def __str__(self):
		return self.subject

	# @property
	# def duration(self):

	# 	return self._duration
	