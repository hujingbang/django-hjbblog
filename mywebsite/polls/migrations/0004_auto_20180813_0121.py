# Generated by Django 2.1 on 2018-08-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_person_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.IntegerField(null=True),
        ),
    ]