# Generated by Django 4.1.5 on 2023-01-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_alter_hackuser_modified_time"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="hackuser",
            options={"ordering": ("country",)},
        ),
        migrations.AlterField(
            model_name="hackuser",
            name="modified_time",
            field=models.CharField(default="01/21/2023 08:40:48 PM", max_length=50),
        ),
        migrations.AlterField(
            model_name="hackuser",
            name="token",
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]