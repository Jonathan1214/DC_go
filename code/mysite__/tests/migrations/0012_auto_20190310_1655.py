# Generated by Django 2.1.2 on 2019-03-10 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_reservation_class_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='fri_res',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='day',
            name='mon_res',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='day',
            name='thurs_res',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='day',
            name='tues_res',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='day',
            name='wed_res',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
