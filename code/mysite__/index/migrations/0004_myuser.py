# Generated by Django 2.1.2 on 2019-10-05 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=10)),
                ('pwd', models.CharField(max_length=100)),
            ],
        ),
    ]
