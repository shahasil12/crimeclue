# Generated by Django 5.1.4 on 2024-12-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clue', '0003_remove_crimereport_class_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='crimereport',
            name='forwarded_to_principal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='crimereport',
            name='investigation_report',
            field=models.TextField(blank=True, null=True),
        ),
    ]
