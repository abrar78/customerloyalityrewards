# Generated by Django 4.0.2 on 2022-02-24 20:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_customer_reward_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swipetime',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 24, 20, 44, 16, 381675)),
        ),
    ]