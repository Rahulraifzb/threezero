# Generated by Django 3.2.6 on 2021-09-09 07:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examdate',
            name='exam_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
