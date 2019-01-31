# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models


class DanceClass(models.Model):

    DAYS_OF_WEEK  = ( ('Monday', 'Monday'),
                      ('Tuesday', 'Tuesday'),
                      ('Wednesday', 'Wednesday'),
                      ('Thursday', 'Thursday'),
                      ('Friday', 'Friday'),
                      ('Saturday', 'Saturday') )

    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=100, default="", null=True, blank=True)
    max_students = models.IntegerField(default=0)
    recital = models.TextField(default="")
    start_day = models.DateField(null=True)
    end_day = models.DateField(null=True)
    age_range = models.CharField(max_length=10, null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK, null=True) 
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    cost = models.IntegerField(default=0)

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
        ('Registered', 'Registered'),
        ('Unpaid', 'Unpaid')
    )

    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_FIELDS, default='Unregistered')
    parent = models.ForeignKey('Parent', null=True, blank=True)
    class_type = models.CharField(max_length=20, blank=True)
    birth_date = models.CharField(max_length=50, null=True, blank=True)
    medical = models.TextField(null=True, blank=True)

    def __repr__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.name:
            return self.name
        else:
            return "Unknown"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.name:
            return self.name
        else:
            return "Unknown"


class Parent(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=75, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    secondary_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __repr__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.name:
            return self.name
        else:
            return "Unknown"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.name:
            return self.name
        else:
            return "Unknown"

class Enrollment(models.Model):
    student = models.ForeignKey('Student')
    dance_class = models.ForeignKey('DanceClass')

    def __repr__(self):
        return str(self.student.name) + " : " + self.dance_class.title + " @ " + str(self.dance_class.start_time)

    def __str__(self):
        return str(self.student.name) + " : " + self.dance_class.title + " @ " + str(self.dance_class.start_time)
    

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
        return "%s %s (%i)" % (self.first_name, self.last_name, self.num_children)

    def __str__(self):
        return "%s %s (%i) - %s" % (self.first_name, self.last_name, self.num_children, self.email)

class Email(models.Model):
    name = models.EmailField(unique=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
