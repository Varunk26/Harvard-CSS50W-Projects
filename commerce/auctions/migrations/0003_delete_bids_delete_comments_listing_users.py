# Generated by Django 4.1.7 on 2023-04-14 06:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_bids_comments_listing"),
    ]

    operations = [
        migrations.DeleteModel(
            name="bids",
        ),
        migrations.DeleteModel(
            name="comments",
        ),
        migrations.AddField(
            model_name="listing",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="listings", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
