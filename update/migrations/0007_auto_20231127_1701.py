# Generated by Django 3.2.23 on 2023-11-27 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('update', '0006_auto_20231126_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personallink',
            name='id',
        ),
        migrations.AddField(
            model_name='personallink',
            name='link_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
