# Generated by Django 5.0 on 2024-01-09 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_transaction_transactions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='ammount',
            new_name='amount',
        ),
    ]