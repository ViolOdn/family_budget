from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    #family_id = models.object.id
    family_id = models.IntegerField(default=1)
    family_name = models.ForeignKey(User, on_delete=models.CASCADE)
    family_email = models.CharField(max_length=100, default="")
    password_hash = models.CharField(max_length=500, default="")

    def __repr__(self):
        return self.family_name + ' ' + self.password_hash


class FamilyMembers(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, default=1)
    family_member_id = models.IntegerField(blank=True)
    family_member_name = models.CharField(max_length=100)
    family_member_description = models.CharField(max_length=100)


class Categories(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, default=1)
    #type_id = models.IntegerField(default=1)
    type_name = models.CharField(max_length=50)


class FlowOfFunds(models.Model):
    family_member_id = models.ForeignKey(Family, on_delete=models.CASCADE, default=1)
    sum = models.FloatField(default=0)
    type_id = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=100)
    date = models.DateField()
    is_it_expense = models.BooleanField(default=True)


class ExpensesPlan(models.Model):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, default=1)
    type_id = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    sum_plan = models.FloatField(default=0)
    start_date = models.DateField()
    finish_date = models.DateField()
