# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(DanceClass)
admin.site.register(Teacher)
admin.site.register(Assignment)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Parent)
admin.site.register(Rsvp)
