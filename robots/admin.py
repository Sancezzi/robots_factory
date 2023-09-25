from django.contrib import admin

from .models import Robot


# Register your models here.
@admin.register(Robot)
class Robots(admin.ModelAdmin):
    fields = ('serial', 'model', 'version', 'created',)
    list_display = ('serial', 'model', 'version', 'created',)