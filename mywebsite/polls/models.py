from django.db import models

# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.IntegerField(null=True)
    create_time = models.DateTimeField(null=True)