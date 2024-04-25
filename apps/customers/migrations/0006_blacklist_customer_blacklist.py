# Generated by Django 5.0.4 on 2024-04-25 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0005_alter_customer_groups_keywords_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blacklist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.category",
                        verbose_name="Black list category",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customer",
            name="blacklist",
            field=models.ManyToManyField(blank=True, related_name="blacklist", to="customers.blacklist"),
        ),
    ]
