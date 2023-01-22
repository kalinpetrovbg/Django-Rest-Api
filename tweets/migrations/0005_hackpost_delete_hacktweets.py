# Generated by Django 4.1.5 on 2023-01-21 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_hackuser_modified_time"),
        ("tweets", "0004_alter_hacktweets_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="HackPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=100, null=True)),
                (
                    "time",
                    models.CharField(default="01/21/2023 04:12:44 PM", max_length=50),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.hackuser"
                    ),
                ),
                (
                    "like",
                    models.ManyToManyField(
                        related_name="liked_users", to="users.hackuser"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="HackTweets",
        ),
    ]