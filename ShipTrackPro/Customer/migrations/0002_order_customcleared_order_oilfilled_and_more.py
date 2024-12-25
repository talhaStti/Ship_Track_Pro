# Generated by Django 5.0.1 on 2024-02-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customCleared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='oilFilled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='tankerDropedAtPort',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='tankerPicked',
            field=models.BooleanField(default=False),
        ),
    ]