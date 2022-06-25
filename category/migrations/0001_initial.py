# Generated by Django 4.0.5 on 2022-06-25 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('repository', '0011_remove_record_category_remove_record_repository_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('record_type', models.CharField(choices=[('input', 'دریافتی'), ('output', 'مخارج')], max_length=30)),
                ('repository',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
        ),
    ]