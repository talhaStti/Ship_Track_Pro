# Generated by Django 5.0.1 on 2024-02-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0013_order_shippingmanifest'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sealContainerNumber',
            field=models.FileField(blank=True, null=True, upload_to='sealContainerNumber/'),
        ),
        migrations.AddField(
            model_name='order',
            name='vesselInformation',
            field=models.FileField(blank=True, null=True, upload_to='vesselInformation/'),
        ),
    ]
