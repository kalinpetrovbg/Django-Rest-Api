# Generated by Django 4.1.5 on 2023-01-21 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_hackuser_modified_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hackuser",
            name="blocked",
        ),
        migrations.RemoveField(
            model_name="hackuser",
            name="following",
        ),
        migrations.AlterField(
            model_name="hackuser",
            name="modified_time",
            field=models.CharField(default="01/21/2023 02:00:00 PM", max_length=50),
        ),
    ]