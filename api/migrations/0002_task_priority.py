# Generated by Django 3.1.7 on 2021-03-31 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
