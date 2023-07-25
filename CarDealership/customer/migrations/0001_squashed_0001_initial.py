# Generated by Django 4.2.3 on 2023-07-25 22:52

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    replaces = [('customer', '0001_initial')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('role', models.CharField(choices=[('customer', 'customer'), ('dealership_admin', 'dealership_admin'), ('superuser', 'superuser')], default='customer', max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('balance', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('location', django_countries.fields.CountryField(blank=True, max_length=15, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.DateField(blank=True, max_length=8, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BuyingHistoryCustomer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
    ]
