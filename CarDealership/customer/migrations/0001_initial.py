# Generated by Django 4.2.2 on 2023-06-25 00:21

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingHistoryCustomer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('contact_number', models.CharField(max_length=13)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
