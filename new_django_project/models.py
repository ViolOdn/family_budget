from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import utils

'''
class Family(models.Model):
    family_id = models.IntegerField(default=1)
    family_name = models.ForeignKey(User, on_delete=models.CASCADE)
    family_email = models.CharField(max_length=100, default="")
    password_hash = models.CharField(max_length=500, default="")

    def __repr__(self):
        return self.family_name + ' ' + self.password_hash
'''

'''
class FamilyMembers(models.Model):
    #family_member_id = models.IntegerField(blank=True)
    family_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    family_member_name = models.CharField(max_length=100)
    family_member_description = models.CharField(max_length=100)
'''

class Categories(models.Model):
    family_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type_id = models.IntegerField(default=1)
    type_name = models.CharField(max_length=50)
    is_it_expense = models.BooleanField(default=True)


class FlowOfFunds(models.Model):
    family_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    #family_member_id = models.ForeignKey(FamilyMembers, on_delete=models.CASCADE, default=1)
    sum = models.FloatField(default=0)
    type_id = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=100)
    #date = models.DateField(default=datetime.date(datetime.today()))
    date = models.DateField(default=utils.timezone.now)


class ExpensesPlan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    sum_plan = models.FloatField(default=0)
    start_date = models.DateField()
    finish_date = models.DateField()


class SavingMoney(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    euro = models.FloatField(default=0)
    dollars = models.FloatField(default=0)
    days_before_salary = models.IntegerField(default=0)

'''
class Human(models.Model):
    name = models.TextField(max_length=50)
    age = models.IntegerField(default=1)
'''