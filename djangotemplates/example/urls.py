from django.conf.urls import url
from example import views
from django.urls import path
from . import views

urlpatterns = [
 
    path('', views.profile),

]