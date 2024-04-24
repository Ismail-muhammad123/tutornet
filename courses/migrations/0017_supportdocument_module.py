# Generated by Django 4.1 on 2023-03-04 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_course_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportdocument',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources', to='courses.module'),
        ),
    ]
