# Generated by Django 3.2.23 on 2023-11-24 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('update', '0002_workhistory_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='current_title',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
