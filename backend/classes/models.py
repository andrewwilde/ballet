# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models


class DanceClass(models.Model):

    DAYS_OF_WEEK  = ( ('Mon', 'Monday'),
                      ('Tue', 'Tuesday'),
                      ('Wed', 'Wednesday'),
                      ('Thu', 'Thursday'),
                      ('Fri', 'Friday'),
                      ('Sat', 'Saturday') )

    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=100, default="")
    max_students = models.IntegerField(default=0)
    recital = models.TextField(default="")
    start_day = models.DateField(null=True)
    end_day = models.DateField(null=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=True) 
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __repr__(self):
        return self.title + " on " + str(self.day_of_week) + ' @ ' + str(self.start_time)

    def __str__(self):
        return self.title + " on " + str(self.day_of_week) + ' @ ' + str(self.start_time)


class Teacher(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class Student(models.Model):
    STATUS_FIELDS = (
        ('Unregistered', 'Unregistered'),
        ('Pre-Registered', 'Pre-Registered'),
        ('Registered', 'Registered')
    )

    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_FIELDS, default='Unregistered')
    parent = models.ForeignKey('Parent', null=True)
    class_type = models.CharField(max_length=20)

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class Parent(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class Enrollment(models.Model):
    student = models.ForeignKey('Student')
    dance_class = models.ForeignKey('DanceClass')

    def __repr__(self):
        return self.student.first_name + " " + self.student.last_name + " is taking " + self.dance_class.title

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + " is taking " + self.dance_class.title
    

class Assignment(models.Model):
    teacher = models.ForeignKey('Teacher')
    dance_class = models.ForeignKey('DanceClass')

    def __repr__(self):
        return self.teacher.first_name + " " + self.teacher.last_name + " teaches " + self.dance_class.title

    def __str__(self):
        return self.teacher.first_name + " " + self.teacher.last_name + " teaches " + self.dance_class.title

class Rsvp(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    num_children = models.IntegerField()

    def __repr__(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name
