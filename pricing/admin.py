from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.Plan)
admin.site.register(models.planfeaters)
admin.site.register(models.bookingplans)