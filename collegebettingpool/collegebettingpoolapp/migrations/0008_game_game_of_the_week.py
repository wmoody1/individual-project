# Generated by Django 2.1.1 on 2018-11-04 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegebettingpoolapp', '0007_auto_20181031_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_of_the_week',
            field=models.BooleanField(default=False),
        ),
    ]
