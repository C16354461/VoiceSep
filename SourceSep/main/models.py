from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.BigIntegerField()

class Audio_File(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,)
    path = models.CharField(max_length=64)
    vocals_path = models.CharField(max_length=64)
