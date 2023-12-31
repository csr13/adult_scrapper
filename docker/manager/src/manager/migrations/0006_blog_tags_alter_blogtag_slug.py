# Generated by Django 4.2.3 on 2023-07-11 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_blog_uid_blogtag_uid_dirtyimage_uid_alter_blog_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='manager.blogtag'),
        ),
        migrations.AlterField(
            model_name='blogtag',
            name='slug',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
