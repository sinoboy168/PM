# Generated by Django 3.0.5 on 2020-04-20 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host_management', '0026_auto_20200419_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='入库时间'),
        ),
    ]
