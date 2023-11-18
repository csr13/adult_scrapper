# Generated by Django 4.2.3 on 2023-07-21 09:19

from django.db import migrations, models
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_dirtyimage_parent_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=manager.models.new_uid, max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='categories',
            field=models.ManyToManyField(blank=True, to='manager.category'),
        ),
    ]