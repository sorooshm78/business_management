# Generated by Django 4.0.5 on 2022-06-25 14:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('repository', '0010_remove_record_category_display'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='category',
        ),
        migrations.RemoveField(
            model_name='record',
            name='repository',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
    ]
