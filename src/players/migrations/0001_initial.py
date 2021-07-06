# Generated by Django 3.2 on 2020-11-05 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('team', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'players',
            },
        ),
    ]
