# Generated by Django 5.0.1 on 2024-02-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0002_order_customcleared_order_oilfilled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='oilReqSent',
            field=models.BooleanField(default=False),
        ),
    ]
