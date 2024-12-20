# Generated by Django 5.0 on 2024-01-06 15:19

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_account_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='recommeded_by',
            new_name='recommended_by',
        ),
        migrations.AlterField(
            model_name='account',
            name='account_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=7, max_length=25, prefix='DEX', unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=10, max_length=25, prefix='217', unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='red_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh1234567890', length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.AlterField(
            model_name='kyc',
            name='identity_image',
            field=models.ImageField(blank=True, null=True, upload_to='kyc'),
        ),
        migrations.AlterField(
            model_name='kyc',
            name='identity_type',
            field=models.CharField(choices=[('national_id_card', 'Natonal ID Card'), ('drivers_licence', 'Drivers Licence'), ('international_passport', 'International Passport'), ('aadhar_card', 'Aadhar Card')], max_length=140),
        ),
    ]
