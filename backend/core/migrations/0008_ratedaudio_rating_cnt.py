# Generated by Django 3.2.4 on 2021-07-12 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_rating_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratedaudio',
            name='rating_cnt',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]