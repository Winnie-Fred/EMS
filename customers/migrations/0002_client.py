# Generated by Django 3.2 on 2023-03-04 22:17

from django.db import migrations, models
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('paid_until', models.DateField()),
                ('on_trial', models.BooleanField()),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
