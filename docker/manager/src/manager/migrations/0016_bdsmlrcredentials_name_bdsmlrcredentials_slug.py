# Generated by Django 4.2.4 on 2023-08-09 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_bdsmlrcredentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='bdsmlrcredentials',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bdsmlrcredentials',
            name='slug',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]