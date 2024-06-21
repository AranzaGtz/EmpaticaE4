from django.db import models

# Create your models here.
from django.db import models

class Session(models.Model):
    device_id = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()

class Acceleration(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

class BVP(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

# Repetir para otros tipos de datos (EDA, HR, IBI, TEMP)

class EDA(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

class HR(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

class IBI(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    duration = models.FloatField()

class TEMP(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()
