# Generated by Django 3.2.23 on 2023-11-26 13:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('update', '0005_auto_20231124_1643'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('user', 'link')},
        ),
        migrations.AlterUniqueTogether(
            name='workhistory',
            unique_together={('user', 'start_date', 'end_date')},
        ),
    ]
