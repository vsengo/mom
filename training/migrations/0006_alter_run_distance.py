# Generated by Django 4.1.1 on 2022-12-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0005_alter_run_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='distance',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]