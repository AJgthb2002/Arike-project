# Generated by Django 4.0.3 on 2022-03-03 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arikeapp', '0007_alter_patient_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='landmark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
