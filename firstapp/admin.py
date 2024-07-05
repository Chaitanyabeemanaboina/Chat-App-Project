from django.contrib import admin
from .models import Message,Activity,Status
# Register your models here.
class Message_admin(admin.ModelAdmin):
    list_display = ['id','room_name','username','message','image','admin','status','request_grp']
admin.site.register(Message,Message_admin)
class Activity_admin(admin.ModelAdmin):
    list_display = ['id','room_name','username','stage','notification']
admin.site.register(Activity,Activity_admin)

class Status_admin(admin.ModelAdmin):
    list_display = ['username','status']
admin.site.register(Status,Status_admin)