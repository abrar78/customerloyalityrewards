# Generated by Django 4.0.2 on 2022-03-02 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_customer_reward_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='reward_points',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='swipetime',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 2, 12, 51, 12, 41432)),
        ),
    ]
