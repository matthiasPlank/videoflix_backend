# Generated by Django 5.0.1 on 2024-02-05 20:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
                ('created_at', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
