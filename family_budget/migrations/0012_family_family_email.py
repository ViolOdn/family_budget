# Generated by Django 2.1.5 on 2019-01-18 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_budget', '0011_family_family_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='family_email',
            field=models.CharField(default='', max_length=100),
        ),
    ]