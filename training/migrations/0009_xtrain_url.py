# Generated by Django 4.1.1 on 2023-01-02 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_runweek_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='xtrain',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]