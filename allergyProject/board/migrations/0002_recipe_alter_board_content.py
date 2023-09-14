# Generated by Django 4.1.7 on 2023-09-14 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Recipes',
            },
        ),
        migrations.AlterField(
            model_name='board',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='board.recipe'),
        ),
    ]
