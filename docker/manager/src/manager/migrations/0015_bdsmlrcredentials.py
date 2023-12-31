# Generated by Django 4.2.4 on 2023-08-09 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_scrapelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='BdsmlrCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flagged', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Bdsmlr Credential',
                'verbose_name_plural': 'Bdsmlr Credentials',
                'ordering': ('-created_at',),
            },
        ),
    ]
