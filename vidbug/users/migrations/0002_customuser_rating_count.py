# Generated by Django 4.1.7 on 2023-04-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rating_count',
            field=models.IntegerField(default=0, verbose_name='rating_count'),
        ),
    ]
