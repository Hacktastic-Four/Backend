# Generated by Django 4.1.7 on 2023-04-01 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_question_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
