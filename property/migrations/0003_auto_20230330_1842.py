# Generated by Django 3.2 on 2023-03-30 17:42

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_auto_20230329_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='for_sale_or_rent',
            field=models.CharField(choices=[('Rent', 'For Rent'), ('Sale', 'For Sale')], max_length=4),
        ),
        migrations.CreateModel(
            name='PropertyVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', cloudinary.models.CloudinaryField(max_length=255, verbose_name='video')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
    ]
