# Generated by Django 2.1.2 on 2019-02-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0009_student_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='res_time',
            field=models.DateTimeField(null=True),
        ),
    ]