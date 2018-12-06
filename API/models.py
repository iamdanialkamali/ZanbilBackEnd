# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Users(User):
    phone_number = models.CharField(max_length=20, blank=True)
    national_code = models.CharField(max_length=10, blank=True)


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Business(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.DO_NOTHING, null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.TextField(max_length=15)
    email = models.EmailField()
    # pics = ArrayField(models.ImageField(blank=True),blank=True,default=[])
    score = models.FloatField(default=0)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=600, default='test')
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING,related_name='businesses')
    #image =models.ImageField(default='2.jpg')

    def __str__(self):
        return self.name

    def calculateScore(self, sc):
        return (self.score + sc) / 2


class TimeTable(models.Model):
    id = models.AutoField(primary_key=True)
    business  = models.ForeignKey(to= Business,on_delete=models.DO_NOTHING,related_name='timetables')
    sans_count = models.IntegerField()
    # work_days = ArrayField(models.IntegerField(blank=True), blank=True)
    # rest_times = ArrayField(models.IntegerField(blank=True), blank=True)


class Sans(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.CharField(default="00:00",max_length=5)
    end_time = models.CharField(default="00:00",max_length=5)
    timetable = models.ForeignKey(to=TimeTable, on_delete=models.DO_NOTHING,related_name='sanses')
    weekday = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.start_time) + 'to' + str(self.end_time)


class Services(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING,related_name='services')
    name = models.CharField(max_length=30)
    # pics = ArrayField(models.ImageField(blank=True),blank=True,default=[])
    fee = models.FloatField()
    timetable = models.ForeignKey(TimeTable, on_delete=models.DO_NOTHING)
    rating = models.FloatField(default=0)
    description = models.TextField(max_length=600, blank=True)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Reserves(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    service = models.ForeignKey(to=Services, on_delete=models.DO_NOTHING, null=True)
    sans = models.ForeignKey(Sans, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField()
    date = models.CharField(max_length=150)




class Review(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=600, default='test')
    rating = models.FloatField()
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING,related_name='reviews')
    service = models.ForeignKey(Services, on_delete=models.DO_NOTHING,related_name='reviews')

    def __str__(self):
        return self.description


class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, max_length=200)
    Business = models.ForeignKey(to=Business, on_delete=models.DO_NOTHING, null=True, related_name='business')
    Service = models.ForeignKey(to=Services, on_delete=models.DO_NOTHING, null=True, related_name='service')
    image = models.ImageField(blank=True)

class Test(models.Model):
    name = models.CharField(max_length =100)
    image = models.ImageField()
