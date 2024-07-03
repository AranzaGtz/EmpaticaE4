# Generated by Django 5.0.6 on 2024-07-03 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e4data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalisisFrecuenciaCardiaca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promedio', models.FloatField()),
                ('mediana', models.FloatField()),
                ('maximo', models.FloatField()),
                ('minimo', models.FloatField()),
                ('fecha_analisis', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
