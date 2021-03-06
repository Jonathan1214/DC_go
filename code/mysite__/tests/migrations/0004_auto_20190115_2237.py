# Generated by Django 2.1.2 on 2019-01-15 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_auto_20190108_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_name', models.CharField(max_length=10)),
                ('class1_available', models.BooleanField()),
                ('class2_available', models.BooleanField()),
                ('class3_available', models.BooleanField()),
                ('class4_available', models.BooleanField()),
                ('start', models.TimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Lab')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Student')),
                ('yiqi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Instrument')),
            ],
        ),
        migrations.AddField(
            model_name='lab',
            name='yuyue',
            field=models.ManyToManyField(through='tests.Reservation', to='tests.Student'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='to_lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Lab'),
        ),
        migrations.AddField(
            model_name='day',
            name='day_to_lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Lab'),
        ),
    ]
