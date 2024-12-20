# Generated by Django 5.0 on 2024-01-06 15:44

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_rename_recommeded_by_account_recommended_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=7, max_length=25, prefix='RR', unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=10, max_length=25, prefix='207', unique=True),
        ),
    ]
