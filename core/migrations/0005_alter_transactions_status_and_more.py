# Generated by Django 5.0 on 2024-01-13 19:43

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_transactions_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='status',
            field=models.CharField(choices=[('failed', 'Failed'), ('completed', 'Completed'), ('pending', 'Pending'), ('processing', 'Processing'), ('request_sent', 'request_sent'), ('request_settled', 'request settled'), ('request_processing', 'request processing')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='transaction_type',
            field=models.CharField(choices=[('transfer', 'Transfer'), ('received', 'Received'), ('withdraw', 'Withdraw'), ('refund', 'Refund'), ('request', 'Payment Request'), ('none', 'None')], default='none', max_length=100),
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=20, prefix='CARD', unique=True)),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('card_type', models.CharField(choices=[('master', 'master'), ('visa', 'visa'), ('verve', 'verve'), ('rupay', 'rupay')], default='rupay', max_length=20)),
                ('card_status', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]