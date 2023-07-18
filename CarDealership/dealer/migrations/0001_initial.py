# Generated by Django 4.2.3 on 2023-07-18 00:13

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dealership", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dealer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                ("amount_of_client", models.PositiveIntegerField(default=0)),
                ("location", django_countries.fields.CountryField(max_length=2)),
                ("contact_number", models.CharField(max_length=13)),
                ("discount_program", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="PromotionDealership",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                ("date_start", models.DateField(max_length=8)),
                ("date_finish", models.DateField(max_length=8)),
                ("description", models.CharField(max_length=500)),
                ("percentage", models.IntegerField(default=0)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "dealership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.dealership",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.model",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PromotionDealer",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                ("date_start", models.DateField(max_length=8)),
                ("date_finish", models.DateField(max_length=8)),
                ("description", models.CharField(max_length=500)),
                ("percentage", models.IntegerField(default=0)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dealer.dealer"
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.model",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DealerInventory",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("price", models.PositiveIntegerField()),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dealer.dealer"
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.model",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BuyingHistoryDealer",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.PositiveIntegerField()),
                (
                    "car",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dealership.car"
                    ),
                ),
                (
                    "dealer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dealer.dealer"
                    ),
                ),
                (
                    "dealership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dealership.dealership",
                    ),
                ),
            ],
        ),
    ]
