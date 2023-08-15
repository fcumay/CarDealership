# Generated by Django 4.2.4 on 2023-08-14 23:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('drivetrain', models.CharField(choices=[('FWD', 'FWD'), ('AWD', 'AWD'), ('RWD', 'RWD'), ('4WD', '4WD')], default='FWD', max_length=20)),
                ('engine', models.CharField(choices=[('Diesel', 'Diesel'), ('Petrol', 'Petrol'), ('Electric', 'Electric'), ('Natural', 'Natural'), ('Gas', 'Gas'), ('Hydrogen', 'Hydrogen'), ('LPG', 'LPG'), ('Flex-fuel', 'Flex-fuel')], default='Petrol', max_length=20)),
                ('bodytype', models.CharField(choices=[('Hatchback', 'Hatchback'), ('Sedan', 'Sedan'), ('SUV', 'SUV'), ('MUV', 'MUV'), ('Coupe', 'Coupe'), ('Convertible', 'Convertible'), ('Pickup', 'Pickup'), ('Truck', 'Truck')], default='Sedan', max_length=20)),
                ('transmission', models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual'), ('CVT', 'CVT')], default='Automatic', max_length=20)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dealership.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Dealership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('balance', models.PositiveIntegerField(default=100)),
                ('location', django_countries.fields.CountryField(max_length=15)),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('discount_program', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dealership.brand')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField()),
                ('customer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dealership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dealership.dealership')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dealership.model')),
            ],
        ),
    ]
