# Generated by Django 5.1.3 on 2024-11-09 13:49

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='NYSC_catego_name_94bb40_idx')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('Quality Nysc Kakhi', 'Quality Nysc Kakhi'), ('Quality Nysc Vest', 'Quality Nysc Vest'), ('Quality Nysc Cap', 'Quality Nysc Cap')], max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.URLField(max_length=600)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('size', models.CharField(max_length=11)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('kakhi', 'kakhi'), ('vest', 'vest'), ('cap', 'cap')], max_length=20)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='NYSC.category')),
            ],
        ),
    ]
