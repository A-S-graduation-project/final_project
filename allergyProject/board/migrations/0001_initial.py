# Generated by Django 4.1.7 on 2023-10-10 07:37

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('bno', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=8, null=True)),
                ('cno', models.CharField(max_length=8, null=True)),
                ('allerinfo', models.TextField()),
                ('cdate', models.DateField()),
                ('ingredient', models.JSONField()),
                ('content', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), size=None)),
            ],
            options={
                'db_table': 'boards',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('serialno', models.AutoField(primary_key=True, serialize=False)),
                ('cno', models.CharField(max_length=8)),
                ('cdate', models.DateField(blank=True, null=True)),
                ('udate', models.DateField(blank=True, null=True)),
                ('comments', models.CharField(max_length=500, null=True)),
                ('bno', models.ForeignKey(db_column='bno', on_delete=django.db.models.deletion.CASCADE, related_name='board', to='board.board')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.AddField(
            model_name='board',
            name='images',
            field=models.ManyToManyField(blank=True, to='board.image'),
        ),
    ]
