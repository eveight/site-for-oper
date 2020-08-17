from django.contrib import admin
from . import models
from .models import Outlet, HistoryGiveUser, Task, Refund, ForUser
# Register your models here.


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ('name', 'view', 'working')
    list_filter = ('view', 'working')


@admin.register(HistoryGiveUser)
class HistoryOutletAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'give_outlet', 'give_user')
    list_filter = ('date_time', 'give_outlet', 'give_user')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'operator', 'outlet', 'status')
    list_filter = ('date_time', 'operator', 'outlet', 'status')


@admin.register(Refund)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'date_achieve', 'user', 'status')
    list_filter = ('date', 'date_achieve', 'user', 'status')


@admin.register(ForUser)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'refund')
    list_filter = ('user', 'refund')


admin.site.register(models.HelpTable)
admin.site.register(models.ForFile)
