# Generated by Django 2.2 on 2019-05-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsale',
            name='units_sold_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
