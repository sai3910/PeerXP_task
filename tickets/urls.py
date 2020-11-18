from django.urls import path
from . import views

urlpatterns = [
    # path('index', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('', views.index, name='index'),
    # path('data', views.pivot_data, name='pivot_data'),
    path('add_ticket', views.addTicket, name='add_ticket'),
    # path('email', views.sendEmail, name='email'),
    # path('register',views.userRegistration, name='userRegistration'),
    path('login',views.userLogin, name='userLogin'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('logout', views.logout, name='logout')
]