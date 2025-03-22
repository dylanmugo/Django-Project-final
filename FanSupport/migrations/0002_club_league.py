# Generated by Django 5.1.7 on 2025-03-12 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FanSupport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='league',
            field=models.CharField(choices=[('PL', 'Premier League'), ('LI', 'League of Ireland')], default='PL', max_length=2),
        ),
    ]
