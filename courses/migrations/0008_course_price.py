# Generated by Django 4.1 on 2022-08-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_course_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.FloatField(default=123456),
            preserve_default=False,
        ),
    ]
