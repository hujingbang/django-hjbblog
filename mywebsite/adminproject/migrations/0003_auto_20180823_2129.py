# Generated by Django 2.1 on 2018-08-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminproject', '0002_auto_20180813_0254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classify_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='acticle',
            name='c_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='acticle',
            name='create_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='acticle',
            name='read_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='acticle',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='acticle',
            name='uploads_file',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
