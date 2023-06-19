# Generated by Django 4.2.2 on 2023-06-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_price_alter_listing_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(max_length=300, unique=True, verbose_name='URL part (slug)'),
        ),
    ]
