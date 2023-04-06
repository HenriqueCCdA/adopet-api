# Generated by Django 4.1.7 on 2023-04-04 22:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"ordering": ("-created_at",), "verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_shelter",
            field=models.BooleanField(default=False, verbose_name="Schelter"),
        ),
    ]