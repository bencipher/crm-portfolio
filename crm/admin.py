from django.contrib import admin
from .models import Agent, Lead

# Register your models here.
admin.site.register((Agent, Lead))
