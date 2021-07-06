# Generated by Django 3.1.3 on 2020-11-29 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20201106_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchPlayers',
            fields=[
                ('player_id', models.IntegerField(primary_key=True, serialize=False)),
                ('season_id', models.CharField(max_length=10)),
                ('team_id', models.IntegerField()),
                ('player_name', models.CharField(max_length=30)),
                ('points', models.IntegerField()),
            ],
            options={
                'db_table': 'Player',
                'managed': False,
            },
        ),
    ]