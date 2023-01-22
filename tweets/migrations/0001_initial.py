# Generated by Django 4.1.5 on 2023-01-21 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HackTweets",
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
                ("tweet_text", models.CharField(max_length=100, null=True)),
                (
                    "time",
                    models.CharField(default="01/21/2023 12:29:36 PM", max_length=50),
                ),
                ("comment", models.CharField(max_length=100, null=True)),
                (
                    "like",
                    models.ManyToManyField(
                        related_name="liked_users", to="users.hackuser"
                    ),
                ),
                ("reply", models.ManyToManyField(to="tweets.hacktweets")),
                (
                    "retweet",
                    models.ManyToManyField(
                        related_name="retweeted_users", to="users.hackuser"
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.hackuser"
                    ),
                ),
            ],
        ),
    ]