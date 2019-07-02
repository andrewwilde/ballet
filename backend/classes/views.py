# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import ( Student, 
                      Parent, 
                      Rsvp, 
                      DanceClass, 
                      Enrollment,
                      Email,
                      Location )

logger = logging.getLogger('ballet')

@api_view(['GET'])
def home(request):
    return render(request, 'front/index.html')

@api_view(['GET'])
def payment(request):
    return render(request, 'front/payment.html')

@api_view(['GET'])
def location(request):
    response_dict = {}

    for cls in DanceClass.objects.all():
        response_dict[cls.id] = { 'city': cls.location.city,
                                        'zipcode': cls.location.zipcode,
                                        'street': cls.location.street }

    return Response(response_dict) 

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

@api_view(['GET'])
def tuition_cost(request):
    class_selections = request.query_params.get("class_selections", None)
    if not class_selections:
        return Response("You must select at least one class.")

    classes = class_selections.split(',')

    if len(classes) > 4:
        logger.error("Someone was able to get around student registration max (more than 4 students).")
        return Response("Unable to process request.", status=400)

    total = 0;
    for selection in classes:
        try:
            total = total + DanceClass.objects.get(id=selection).cost
        except Exception as e:
            logger.error("WARNING: There was an issue getting the tuition cost. Failed on value %s. exception=%s" % ( str(selection), str(e)) )
            return Response("There was a problem getting the tuition total.", status=400)

    return Response(total)
    
@api_view(['GET'])
def classes(request):
    dance_classes = []
    for dance_class in DanceClass.objects.all():
        count = Enrollment.objects.filter(dance_class__id=dance_class.id).count()
        has_room = True if count < dance_class.max_students else False
        dance_classes.append( {'id': dance_class.id, 
                               'title': dance_class.title,
                               'day_of_week': dance_class.get_day_of_week_display(),
                               'start_time': str(dance_class.start_time).rpartition(':')[0],
                               'end_time': str(dance_class.end_time).rpartition(':')[0],
                               'start_day': dance_class.start_day,
                               'range': dance_class.age_range,
                               'has_room': has_room,
                               'open_spots': dance_class.max_students - count } )

    return Response(dance_classes)
  
@api_view(['POST'])
def email_signup(request):
    logger.info("Verifying newsletter signup... data=%s" % str(request.data))
    email = request.data.get('email_reg', None)

    if email:
        if Email.objects.filter(name=email):
            return render(request, 'front/email_confirmed.html')
        else: 
            try:
                email_obj = Email(name=email)
                email_obj.full_clean()
                email_obj.save()
            except ValidationError:
                logger.error("Integrity Error saving the following email: %s" % email)
                return render(request, 'front/email_failed.html') 
    else:
        logger.error("Newsletter signup didn't have the email field filled out.")
        return render(request, 'front/email_failed.html')

    return render(request, 'front/email_confirmed.html')
 
@api_view(['POST'])
def verify_reg_data(request):
    logger.info("Verifying the following request: %s" % str(request.data))
    students = request.data.get('students', None)
    registration_fee = request.data.get('reg_fee', None)
    tuition_fee = request.data.get('tuition_fee', None)
    total_fee = request.data.get('total_fee', None)

    #Do we have all the required parent variables?
    if not (students and registration_fee and tuition_fee and total_fee):
        logger.error( "One of the required POST variables was not provided. students=%s, reg_fee=%s, tuition_fee=%s, total_fee=%s." % \
                                                                          ( str(students), str(registration_fee), str(tuition_fee), str(total_fee) ) )
        return Response(False)
    else:
        students = json.loads(students)

    #Is the registration fee correct?
    if len(students) < 1:
        logger.error( "There must be at least one student. students=%i" % len(students) )
        return Response(False)
    elif len(students) == 1 and int(registration_fee) != settings.SINGLE_REG_FEE:
        logger.error( "Registration fee is incorrect. Expected=%s, Actual=%s" % (settings.SINGLE_REG_FEE, int(registration_fee)) )
        return Response(False)
    elif len(students) > 1 and int(registration_fee) != settings.MULTI_REG_FEE:
        logger.error( "Registration fee is incorrect (multi). Expected=%s, Actual=%s" % (settings.MULTI_REG_FEE, int(registration_fee)) )     
        return Response(False)

    #Is there enough room in the classes?
    reg_classes = {}
    for student in students:
        class_id = student.get('class_id', None)
        if not class_id:
            logger.error("Class ID not included in student data.")
            return Response(False)

        if class_id not in reg_classes:
            reg_classes[class_id] = 1
        else:
            reg_classes[class_id] = reg_classes[class_id] + 1

    for k,v in reg_classes.items():
        count = Enrollment.objects.filter(dance_class__id=k).count()
        dance_class = DanceClass.objects.get(id=k)
        if dance_class.max_students - count < v:
            logger.error( "There is not enough room in class %s" % str(dance_class) )
            return Response(False)

    #Is the tuition total correct?
    tuition_total = 0
    for student in students:
        class_id = student.get('class_id', None)
        name = student.get('student_name', None)
        birth_date = student.get('birth_date', None) 

        #Do we have all the correct variables for each student?
        if not (class_id and name and birth_date):
            logger.error( "One of the students was not provided with a required variable. student=%s" % str(student) )
            return Response(False)
        
        #Does the class exist?
        try:
            dance_class = DanceClass.objects.get(id=student.get('class_id'))
            tuition_total = tuition_total + dance_class.cost
        except Exception as e:
            logger.error( "Unable to get Dance Class from provided class_id. e=%s" % str(e) )
            return Response(False)

    #Is the tuition total correct?
    if tuition_total != int(tuition_fee):
        logger.error( "Tuition total was not as expected. Expected:%i, Actual=%i" % (tuition_total, int(tuition_fee)) )
        return Response(False)

    #Is the total correct?
    total_check = tuition_total + int(registration_fee)
    if total_check != int(total_fee):
        logger.error( "The total fee was not as expected. Expected:%i, Actual=%i" % (total_check, int(total_fee)) )
        return Response(False)

    return Response(True)
