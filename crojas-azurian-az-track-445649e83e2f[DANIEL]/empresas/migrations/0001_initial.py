# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CamposOpcionalesEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opcional1', models.CharField(db_index=True, max_length=120)),
                ('opcional2', models.CharField(blank=True, db_index=True, max_length=120, null=True)),
                ('opcional3', models.CharField(blank=True, db_index=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('rut', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('empresa', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(db_index=True, max_length=200, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.Holding'),
        ),
        migrations.AddField(
            model_name='camposopcionalesemail',
            name='empresa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='empresas.Empresa'),
        ),
    ]
