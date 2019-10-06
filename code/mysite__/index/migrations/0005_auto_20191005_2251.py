# Generated by Django 2.1.2 on 2019-10-05 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='arthor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.MyUser'),
        ),
        migrations.AddField(
            model_name='img',
            name='up_load_time',
            field=models.DateTimeField(null=True),
        ),
    ]
