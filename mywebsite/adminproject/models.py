from django.db import models

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_time = models.DateTimeField(null=True)


class Acticle(models.Model):
    content = models.TextField(null=True)
    title = models.CharField(max_length=100,null=True)
    c_id = models.IntegerField(null=True)
    uploads_file = models.CharField(max_length=255, null=True)
    read_count = models.IntegerField(null=True)
    create_time = models.DateTimeField(null=True)


class Classify(models.Model):
    classify_name = models.CharField(max_length=100)



