# Generated by Django 2.1.2 on 2019-01-16 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_auto_20190115_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='used',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='day',
            name='class1_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='day',
            name='class2_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='day',
            name='class3_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='day',
            name='class4_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='total',
            field=models.IntegerField(default=4),
        ),
    ]