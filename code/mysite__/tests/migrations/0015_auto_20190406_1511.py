# Generated by Django 2.1.2 on 2019-04-06 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0014_reservation_capta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='pwd',
            field=models.CharField(max_length=100),
        ),
    ]
