# Generated by Django 3.0.5 on 2020-04-21 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_pool', '0007_inspectiontasklist_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspectiontaskcyclesetting',
            old_name='location',
            new_name='point',
        ),
        migrations.RenameField(
            model_name='inspectiontasklist',
            old_name='location',
            new_name='point',
        ),
    ]
