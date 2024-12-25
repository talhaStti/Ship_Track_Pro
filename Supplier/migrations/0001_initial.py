# Generated by Django 5.0.1 on 2024-02-06 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signup', '0002_alter_customer_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='productImages')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.supplier')),
            ],
        ),
    ]