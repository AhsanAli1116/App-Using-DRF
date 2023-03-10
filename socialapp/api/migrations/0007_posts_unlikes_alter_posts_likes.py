# Generated by Django 4.1.5 on 2023-02-02 16:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0006_alter_userdetail_city_alter_userdetail_country_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="unlikes",
            field=models.ManyToManyField(
                blank=True, related_name="blogpost_unlike", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="posts",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="blogpost_like",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
