from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add_ticket', views.addTicket, name='add_ticket'),
    path('login',views.userLogin, name='userLogin'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('logout', views.logout, name='logout')
]