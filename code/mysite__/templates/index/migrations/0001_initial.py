# Generated by Django 2.1.2 on 2019-01-15 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tname', models.CharField(max_length=32)),
                ('teacher', models.ManyToManyField(to='index.Class')),
            ],
        ),
    ]