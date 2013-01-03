# -*- coding: utf-8 -*-
from django.contrib import admin
from dashboard.models import *

admin.site.register(Project)
admin.site.register(UseCase)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Room)
admin.site.register(News)
admin.site.register(Event)