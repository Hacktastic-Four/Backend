# Generated by Django 4.1.7 on 2023-04-01 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
