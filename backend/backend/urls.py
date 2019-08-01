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
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from mezzanine.conf import settings

admin.autodiscover()

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url(r'^admin/', include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
]

urlpatterns += [
    #url(r'^admin/', admin.site.urls),
    url(r'register/preregister', csrf_exempt(registration.pre_register)),
    url(r'^free_class', registration.free_class),
    url(r'^$', registration.home, name='home'),
    url(r'^payment', registration.payment, name='payment'),
    url(r'^tuition_total', registration.tuition_cost, name='tuition'),
    url(r'^verify_reg_data', registration.verify_reg_data, name='verify'),
    url(r'^classes', registration.classes, name='classes'),
    url(r'^location', registration.location, name='location'),
    url(r'^charge', charge.charge, name='charge'),
    url(r'^register', charge.register, name='register'),
    url(r'^email_signup', registration.email_signup, name='email'),
    url(r'^send_mail', registration.send_email, name='send_mail'),

    url(r"^", include("mezzanine.urls")),
]

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
