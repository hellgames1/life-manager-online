from django.db import models

# Create your models here.
class UserSettings(models.Model):
    val1name=models.CharField(max_length=30,default="",blank=True)
    val2name=models.CharField(max_length=30,default="",blank=True)
    val3name=models.CharField(max_length=30,default="",blank=True)
    val4name=models.CharField(max_length=30,default="",blank=True)
    val5name=models.CharField(max_length=30,default="",blank=True)
    val6name=models.CharField(max_length=30,default="",blank=True)
    val7name=models.CharField(max_length=30,default="",blank=True)
    val8name=models.CharField(max_length=30,default="",blank=True)
    val9name=models.CharField(max_length=30,default="",blank=True)
    val1type = models.IntegerField(default=-1)
    val2type = models.IntegerField(default=-1)
    val3type = models.IntegerField(default=-1)
    val4type = models.IntegerField(default=-1)
    val5type = models.IntegerField(default=-1)
    val6type = models.IntegerField(default=-1)
    val7type = models.IntegerField(default=-1)
    val8type = models.IntegerField(default=-1)
    val9type = models.IntegerField(default=-1)
    val1keep = models.IntegerField(default=-1)
    val2keep = models.IntegerField(default=-1)
    val3keep = models.IntegerField(default=-1)
    val4keep = models.IntegerField(default=-1)
    val5keep = models.IntegerField(default=-1)
    val6keep = models.IntegerField(default=-1)
    val7keep = models.IntegerField(default=-1)
    val8keep = models.IntegerField(default=-1)
    val9keep = models.IntegerField(default=-1)
    val1default = models.IntegerField(default=-1)
    val2default = models.IntegerField(default=-1)
    val3default = models.IntegerField(default=-1)
    val4default = models.IntegerField(default=-1)
    val5default = models.IntegerField(default=-1)
    val6default = models.IntegerField(default=-1)
    val7default = models.IntegerField(default=-1)
    val8default = models.IntegerField(default=-1)
    val9default = models.IntegerField(default=-1)
class Day(models.Model):
    descr = models.CharField(max_length=8,default="fixit")
    notes = models.CharField(max_length=30,default="",blank=True)
    int1 = models.IntegerField(default=-1)
    int2 = models.IntegerField(default=-1)
    int3 = models.IntegerField(default=-1)
    int4 = models.IntegerField(default=-1)
    int5 = models.IntegerField(default=-1)
    int6 = models.IntegerField(default=-1)
    int7 = models.IntegerField(default=-1)
    int8 = models.IntegerField(default=-1)
    int9 = models.IntegerField(default=-1)