# Generated by Django 5.0 on 2024-01-06 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_account_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='identity_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='KYC'),
        ),
    ]
