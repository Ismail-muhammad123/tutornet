# Generated by Django 4.1 on 2023-08-15 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_course_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
