# Generated by Django 4.2.3 on 2023-07-25 10:27

from django.db import migrations, models
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_category_blog_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.CharField(max_length=255, null=True, unique=True)),
                ('uid', models.CharField(default=manager.models.new_uid, max_length=255)),
                ('url', models.URLField(max_length=255, null=True)),
                ('streak_limit', models.IntegerField(default=5)),
                ('max_images', models.IntegerField(default=15)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ('-created_at',), 'verbose_name': 'Blog', 'verbose_name_plural': 'Blogs'},
        ),
        migrations.AlterModelOptions(
            name='blogtag',
            options={'ordering': ('-created_at',), 'verbose_name': 'Blog Tag', 'verbose_name_plural': 'Blog Tags'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-created_at',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='dirtyimage',
            options={'ordering': ('-created_at',), 'verbose_name': 'Dirty Image', 'verbose_name_plural': 'Dirty Images'},
        ),
    ]
