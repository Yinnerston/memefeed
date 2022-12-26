# Generated by Django 4.1.4 on 2022-12-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reddit", "0002_alter_submission_media_alter_submission_media_embed_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="media",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="submission",
            name="media_embed",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="submission",
            name="secure_media",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="submission",
            name="secure_media_embed",
            field=models.JSONField(default=dict),
        ),
    ]
