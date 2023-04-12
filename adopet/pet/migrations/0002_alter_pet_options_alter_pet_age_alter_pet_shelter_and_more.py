# Generated by Django 4.1.7 on 2023-04-09 04:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pet", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pet",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AlterField(
            model_name="pet",
            name="age",
            field=models.PositiveSmallIntegerField(verbose_name="Idade"),
        ),
        migrations.AlterField(
            model_name="pet",
            name="shelter",
            field=models.ForeignKey(
                limit_choices_to={"is_active": True, "is_shelter": True, "is_tutor": False},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="size",
            field=models.CharField(
                choices=[("S", "Porte pequeno"), ("M", "Porte Médio"), ("B", "Porte Grande")],
                max_length=1,
                verbose_name="Porte",
            ),
        ),
    ]