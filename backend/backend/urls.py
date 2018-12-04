"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from classes import views as registration
from charge import views as charge
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'register/preregister', csrf_exempt(registration.pre_register)),
    url(r'rsvp', csrf_exempt(registration.rsvp)),
    url(r'^$', registration.home, name='home'),
    url(r'^payment', registration.payment, name='payment'),
    url(r'^tuition_total', registration.tuition_cost, name='tuition'),
    url(r'^verify_reg_data', registration.verify_reg_data, name='verify'),
    url(r'^charge', charge.charge, name='charge'),
    url(r'^register', charge.register, name='register'),
]
