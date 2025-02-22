# Generated by Django 4.1 on 2023-02-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_remove_module_intoduction_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='supportdocument',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='supportdocument',
            name='file',
            field=models.FileField(upload_to='course_support_files'),
        ),
    ]
