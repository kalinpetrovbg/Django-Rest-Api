# Generated by Django 4.1.5 on 2023-01-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tweets", "0010_hackpost_removed_alter_hackpost_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hackpost",
            name="timestamp",
            field=models.CharField(default="01/21/2023 05:16:55 PM", max_length=50),
        ),
    ]