# Generated by Django 4.0.3 on 2022-03-03 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arikeapp', '0004_remove_family_detail_full_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]