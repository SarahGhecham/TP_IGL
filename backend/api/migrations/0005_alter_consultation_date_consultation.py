# Generated by Django 5.1.4 on 2024-12-24 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_examenbiologique_date_examen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='date_consultation',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
