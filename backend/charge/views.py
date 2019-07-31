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

from classes.models import DanceClass, Student, Parent, Enrollment
logger = logging.getLogger('ballet')
admins = logging.getLogger('admins')

if settings.STRIPE_LIVE_MODE:
    stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
else:
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

    students = {}
    for k in request.data.keys():
        if 'student' in k:
            name, _, key = k.rpartition('_')
            if key not in students:
                students[key] = {}
            students[key][name] = request.data.get(k)

    email = request.data.get('reg_email', None)
    payer = request.data.get('payer', None)
    primary_phone = request.data.get('primary_phone', None)
    
    tuition_fee = request.data.get('fee_tuition', None)
    register_fee = request.data.get('fee_register', None)
    total_fee = request.data.get('fee_total', None)

    secondary_phone = request.data.get('secondary_phone', None)
    referral = request.data.get('ref_name', None)

    #Check stripe token
    stripe_token = request.data.get('stripeToken', None)
    if not stripe_token:
        logger.error("Cannot register. There is no token.")
        return Response(status=400)

    #Check parent fields
    if not (email and payer and primary_phone):
        admins.error('WARNING: Missing parent information. email=%s, payer=%s, primary_phone=%s' % (str(email), str(payer), str(primary_phone)))
        return Response(status=400)

    #Check fee fields
    if not (tuition_fee and register_fee and total_fee):
        admins.error('WARNING: Missing fee. tuition=%s, registration=%s, total_fee=%s' & (str(tuition_fee), str(register_fee), str(total_fee)))
        return Response(status=400)

    #Check registration fee number
    registration_check = 0
    if len(students.keys()) == 0:
        admins.error("WARNING: No students registering.")
        return Response(status=400)
    elif len(students.keys()) == 1:
        if int(register_fee) != settings.SINGLE_REG_FEE:
            admins.error("WARNING: Registration fee was incorrect. Expected=%s, Actual=%s" % (str(settings.SINGLE_REG_FEE), str(register_fee)))
            return Response(status=400)
        else:
            registration_check = settings.SINGLE_REG_FEE
    elif len(students.keys()) > 1:
        if int(register_fee) != settings.MULTI_REG_FEE:
            admins.error("WARNING: Registration fee was incorrect. Expected=%s, Actual=%s" % (str(settings.MULTI_REG_FEE), str(register_fee)))
            return Response(status=400)
        else:
            registration_check = settings.MULTI_REG_FEE

    #Check tuition fee number
    validated_students = []
    tuition_check = 0
    for _, student_dict in students.items():
        class_id = student_dict.get('student_class_id', None)
        student_name = student_dict.get('student_name', None)
        birth_date = student_dict.get('student_birth_date', None)
        medical = student_dict.get('student_medical_id', "")

        if not (class_id and student_name and birth_date):
            admins.error("WARNING: One of the students was missing required data. class_id=%s, student_name=%s, birth_date=%s" % (str(class_id), str(student_name), str(birth_date)))
            return Response(status=400)

        try:
            dance_class = DanceClass.objects.get(id=class_id)
            tuition_check = tuition_check + dance_class.cost
            validated_students.append( {"student_name": student_name, "birth_date": birth_date, "class_id": class_id, "medical": medical} )
        except Exception as e:
           admins.error("WARNING: Class does not exist. class=%s, e=%s" % ( str(class_id), str(e) ))
           return Response(status=400)

    if tuition_check != int(tuition_fee):
        admins.error("WARNING: Tuition fee was not correct. Expected=%i, Actual=%i" % ( tuition_check, int(tuition_fee) ))
        return Response(status=400)

    #Check fee totals
    checked_fees = int(tuition_check) + int(registration_check)
    posted_fees = int(tuition_fee) + int(register_fee)
    if not (checked_fees == posted_fees == int(total_fee)):
        admins.error("WARNING: Total fee was not correct. Posted fees=%i, Checked fees=%i, Total posted fees=%i" % (posted_fees, checked_fees, int(total_fee)))
        return Response(status=400)

    #Create Parent
    parent = Parent.objects.create(name=payer, email=email, phone_number=primary_phone, secondary_number=secondary_phone, referral=referral)

    #Create Student
    created_students = []
    for student in validated_students:
        new_student = Student.objects.create(name=student.get("student_name"), birth_date=student.get("birth_date"), status="Unpaid", parent=parent, medical=medical)
        assignment = Enrollment.objects.create(student=new_student, dance_class=DanceClass.objects.get(id=student.get("class_id")))
        created_students.append(new_student)

    #Create payment
    try: 
        customer = stripe.Charge.create(
                       amount=checked_fees*100,
                       currency="USD",
                       description=email,
                       card=stripe_token
                   )
    except Exception as e:
        admins.info("Problem with credit card transaction. e=%s" % str(e))
        student_status = "Unpaid"
        return render(request, 'register/failed.html') 
    else:
        student_status = "Registered"
        return render(request, 'register/confirmed.html')
    finally: 
        for student in created_students:
            student.status=student_status
            student.save()
            admins.info("New student has successfully registered: %s" % str(student.name))
    

