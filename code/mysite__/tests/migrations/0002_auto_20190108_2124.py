# Generated by Django 2.1.2 on 2019-01-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=10)),
                ('student_name', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
