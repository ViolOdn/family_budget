# Generated by Django 2.1.5 on 2019-02-05 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_budget', '0014_auto_20190201_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=100)),
                ('passport_number', models.CharField(max_length=100)),
            ],
        ),
    ]
