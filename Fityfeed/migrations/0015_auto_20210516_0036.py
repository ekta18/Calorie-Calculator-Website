# Generated by Django 3.2 on 2021-05-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Fityfeed', '0014_exercise_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='user',
        ),
        migrations.AddField(
            model_name='exercise',
            name='user_id',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
