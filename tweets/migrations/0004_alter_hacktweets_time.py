# Generated by Django 4.1.5 on 2023-01-21 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0003_alter_hacktweets_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hacktweets",
            name="time",
            field=models.CharField(default="01/21/2023 02:00:00 PM", max_length=50),
        ),
    ]