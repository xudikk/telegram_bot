# Generated by Django 3.1.4 on 2020-12-20 06:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_code', models.CharField(db_index=True, default=None, help_text='ISO 3166-1 alpha 2', max_length=2, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('iso_code3', models.CharField(db_index=True, default=None, help_text='ISO 3166-1 alpha 3', max_length=3, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('name_ru', models.CharField(db_index=True, max_length=100)),
                ('name_uz', models.CharField(db_index=True, max_length=100)),
                ('lat', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude')),
                ('lng', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude')),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name_ru'],
            },
        ),
    ]