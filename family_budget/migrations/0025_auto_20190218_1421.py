# Generated by Django 2.1.5 on 2019-02-18 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family_budget', '0024_auto_20190216_2041'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Human',
        ),
        migrations.AlterField(
            model_name='expensesplan',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family_budget.Categories'),
        ),
    ]