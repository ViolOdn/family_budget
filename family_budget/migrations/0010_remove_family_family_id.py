# Generated by Django 2.1.5 on 2019-01-10 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_budget', '0009_family_family_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='family_id',
        ),
    ]