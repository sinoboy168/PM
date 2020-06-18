# Generated by Django 3.0.5 on 2020-04-20 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('host_management', '0026_auto_20200419_0819'),
        ('task_pool', '0002_inspectiontaskcyclesetting_inspectiontasklist_troublerecord_troubletag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectiontaskcyclesetting',
            name='machine_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspection_machine_area_name', to='host_management.Area', verbose_name='设备所在区域'),
        ),
        migrations.AlterField(
            model_name='inspectiontasklist',
            name='machine_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspection_machine_area_list_name', to='host_management.Area', verbose_name='设备所在区域'),
        ),
    ]
