# Generated by Django 4.0.2 on 2022-02-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_customer_reward_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='reward_points',
            field=models.CharField(default='0', max_length=100),
        ),
    ]