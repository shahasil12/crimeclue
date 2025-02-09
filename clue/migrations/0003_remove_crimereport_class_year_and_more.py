# Generated by Django 5.1.4 on 2024-12-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0002_crimereport_location_crimereport_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crimereport',
            name='class_year',
        ),
        migrations.RemoveField(
            model_name='crimereport',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='crimereport',
            name='resolution',
        ),
        migrations.AddField(
            model_name='crimereport',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='category',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='location',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='proof',
            field=models.FileField(blank=True, null=True, upload_to='proofs/'),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='reported_by',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='crimereport',
            name='year',
            field=models.CharField(default='Unknown', max_length=10),
        ),
    ]
