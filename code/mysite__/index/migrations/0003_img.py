# Generated by Django 2.1.2 on 2019-10-05 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20190115_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/index')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
    ]
