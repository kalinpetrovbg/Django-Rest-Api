# Generated by Django 4.1.5 on 2023-01-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0017_hackuser_name_alter_hackuser_company_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hackuser",
            name="modified_time",
        ),
        migrations.AddField(
            model_name="hackuser",
            name="registered",
            field=models.CharField(default="01/21/2023 08:49:59 PM", max_length=50),
        ),
    ]
