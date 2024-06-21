# Generated by Django 5.0.6 on 2024-06-21 04:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=50)),
                ('session_id', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='IBI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('duration', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
        migrations.CreateModel(
            name='HR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
        migrations.CreateModel(
            name='EDA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
        migrations.CreateModel(
            name='BVP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
        migrations.CreateModel(
            name='Acceleration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
        migrations.CreateModel(
            name='TEMP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('value', models.FloatField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e4data.session')),
            ],
        ),
    ]
