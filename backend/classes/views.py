# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Student, Parent, Rsvp

logger = logging.getLogger('ballet')

@api_view(['GET'])
def home(request):
    return render(request, 'front/index.html')

@api_view(['POST'])
def rsvp(request):
    logger.info("RSVP triggered. request.data=%s" % str(request.data))
    data = { "first_name": request.data.get("first_name", None),
             "last_name": request.data.get("last_name", None),
             "email": request.data.get("email", None),
             "num_children": request.data.get("num_children", None) }

    if None in data.values():
        return Response("Not all required fields were filled out.", status=400)

    data['phone'] = request.data.get("phone", "")

    Rsvp.objects.create(**data)

    return Response("RSVP has been successfully created.")

@api_view(['POST'])
def pre_register(request):
    logger.info(str(request.data))
    data = { "class_type": request.data.get("class_name", None),
             "status" : "Pre-Registered"}

    if not data.get("class_type", None):
        return Response("That class is not valid.", status=400)

    if data.get("class_type") == "adult":
        data["first_name"] = request.data.get("student_first", None)
        data["last_name"] = request.data.get("student_last", None)
        data["email"] = request.data.get("email", None)
        data["phone_number"] = request.data.get("phone", None)

        if None in data.values():
            logger.error("Data incomplete(2): %s" % str(data))
            return Response("Fill out all fields.", status=400)

        Student.objects.create(**data)
    else:
        parent_data = { "first_name": request.data.get("parent_first", None),
                        "last_name" : request.data.get("parent_last", None),
                        "phone_number": request.data.get("phone", None),
                        "email": request.data.get("email", None) }

        if None in parent_data.values():
            logger.error("Parent Data incomplete(3): %s" % str(parent_data))
            return Response("Fill out all fields.", status=400)

        data["first_name"] = request.data.get("student_first", None)
        data["last_name"] = request.data.get("student_last", None)
        data["age"] = int(request.data.get("student_age", None))

        if None in data.values():
            logger.error("Student Data incomplete(4): %s" % str(data))
            return Response("Fill out all fields.", status=400)

        parent = Parent.objects.create(**parent_data)
        data["parent"] = parent

        Student.objects.create(**data)

    return Response("Pre-Reigstration Complete")
