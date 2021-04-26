# Generated by Django 3.1.7 on 2021-03-04 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import yesboss.base.fields
import yesboss.company.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0003_district'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.JSONField(default=yesboss.base.fields.lang_dict_field)),
                ('alias', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=800, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=yesboss.company.models.logo_image_folder)),
                ('lat', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Latitude')),
                ('lng', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True, verbose_name='Longitude')),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('is_terms', models.BooleanField(default=False)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_district', to='geo.district')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_region', to='geo.region')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_company', to='company.statuses')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_company', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
        ),
    ]