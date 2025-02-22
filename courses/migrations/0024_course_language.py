# Generated by Django 3.2.13 on 2023-08-07 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0023_review_profession'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('ha', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pcm', 'Pidgin English'), ('ar', 'Arabic'), ('sw', 'Swahili'), ('am', 'Amharic'), ('so', 'Somali'), ('zu', 'Zulu'), ('fr', 'French'), ('pt', 'Portuguese'), ('af', 'Afrikaans'), ('wo', 'Wolof'), ('om', 'Oromo'), ('ti', 'Tigrinya'), ('ber', 'Berber')], default='en', max_length=5),
        ),
    ]
