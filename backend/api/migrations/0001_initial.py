# Generated by Django 5.1.4 on 2024-12-23 03:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_consultation', models.DateTimeField()),
                ('motif', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nss', models.CharField(max_length=20, unique=True)),
                ('date_naissance', models.DateField()),
                ('adresse', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=15)),
                ('mutuelle', models.CharField(max_length=100)),
                ('personne_a_contacter', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Administratif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_bilan', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='images/radiology/')),
                ('comment', models.TextField(blank=True, null=True)),
                ('consultation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bilanRadiologique', to='api.consultation')),
            ],
        ),
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_bilan', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('consultation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bilanBiologique', to='api.consultation')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='dpi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='api.dpi'),
        ),
        migrations.CreateModel(
            name='ExamenBiologique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_examen', models.CharField(max_length=255)),
                ('resultat', models.FloatField(default=0)),
                ('unite', models.CharField(max_length=50)),
                ('date_examen', models.DateTimeField()),
                ('bilan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examens', to='api.bilanbiologique')),
            ],
        ),
        migrations.CreateModel(
            name='Infirmier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Laborantin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dpi',
            name='medecin_traitant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='api.medecin'),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dpi',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.patient'),
        ),
        migrations.CreateModel(
            name='Radiologue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
