# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 01:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_tag', models.IntegerField()),
                ('seq', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('measureunits', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.IntegerField()),
                ('describe', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='exhibited_picture/%Y/%m/%d')),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('user', models.CharField(blank=True, max_length=40)),
                ('exihibitpic', models.ImageField(upload_to='exhibited_picture/%Y/%m/%d')),
                ('introduce', models.TextField()),
                ('tips', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='exhibited_picture/%Y/%m/%d')),
                ('pubdate', models.DateTimeField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='childrenrecipe.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='childrenrecipe.Category')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='childrenrecipe.Tag'),
        ),
        migrations.AddField(
            model_name='procedure',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='childrenrecipe.Recipe'),
        ),
        migrations.AddField(
            model_name='material',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='childrenrecipe.Recipe'),
        ),
    ]
