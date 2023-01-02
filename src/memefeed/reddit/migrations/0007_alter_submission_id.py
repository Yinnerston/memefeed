# Generated by Django 4.1.4 on 2023-01-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reddit", "0006_alter_submission_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="id",
            field=models.CharField(
                max_length=10,
                primary_key=True,
                serialize=False,
                verbose_name="Reddit post's ID",
            ),
        ),
    ]
