# Generated by Django 3.1.5 on 2021-01-23 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0009_remove_lead_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='description',
        ),
    ]