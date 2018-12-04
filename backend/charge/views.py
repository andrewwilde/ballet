# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import stripe

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

logger = logging.getLogger('ballet')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@api_view(['POST'])
def charge(request, *args, **kwargs):
    stripe_token = request.POST.get('stripeToken', None)
    if not stripe_token:
        Response("Error 101.", status_code=400)

    customer = stripe.Charge.create(
                   amount=1000,
                   currency="USD",
                   description="andrew.wilde@gmail.com",
                   card=stripe_token
               )

    return Response("Success")

@api_view(['POST'])
def register(request, *args, **kwargs):
    logger.info("registering with following data: %s" % str(request.data))
    return render(request, 'register/confirmed.html')

