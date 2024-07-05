from django.db import models

# Create your models here.
class Message(models.Model):
    room_name = models.CharField(max_length=500,null=True)
    username = models.CharField(max_length=400,null=True)
    message = models.CharField(max_length=400,null=True)
    image = models.ImageField(upload_to='images/',null=True,default=None)
    admin = models.BooleanField(null=True)
    status = models.CharField(max_length=400,null=True)
    request_grp = models.CharField(max_length=400, null=True)


class Activity(models.Model):
    room_name = models.CharField(max_length=60,null=True)
    username = models.CharField(max_length=60,null=True)
    stage = models.BooleanField(null=True)
    notification = models.IntegerField(null=True)

class Status(models.Model):
    username = models.CharField(max_length=50,null=True)
    status = models.BooleanField(null=True)
