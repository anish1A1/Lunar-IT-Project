# Generated by Django 5.0.7 on 2024-08-12 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lunarapp', '0007_coursepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_Intern',
            field=models.BooleanField(default=False, help_text='If the user is intern or not'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_Staff',
            field=models.BooleanField(default=False, help_text='If the user is staff or not'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_Student',
            field=models.BooleanField(default=False, help_text='If the user is student or not'),
        ),
    ]
