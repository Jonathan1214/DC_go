# Generated by Django 2.1.2 on 2019-02-28 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_reservation_res_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='class_id',
            field=models.IntegerField(null=True),
        ),
    ]
