# Generated by Django 3.1.3 on 2020-11-30 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0005_teams'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('player_id', models.IntegerField(primary_key=True, serialize=False)),
                ('season_id', models.CharField(max_length=10)),
                ('league_id', models.IntegerField()),
                ('team_id', models.IntegerField()),
                ('team_abbr', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('gp', models.IntegerField(blank=True, db_column='GP', null=True)),
                ('gs', models.IntegerField(blank=True, db_column='GS', null=True)),
                ('min', models.IntegerField(blank=True, db_column='MIN', null=True)),
                ('fgm', models.IntegerField(blank=True, db_column='FGM', null=True)),
                ('fga', models.IntegerField(blank=True, db_column='FGA', null=True)),
                ('fg_pct', models.FloatField(blank=True, db_column='FG_PCT', null=True)),
                ('fg3m', models.IntegerField(blank=True, db_column='FG3M', null=True)),
                ('fg3a', models.IntegerField(blank=True, db_column='FG3A', null=True)),
                ('fg3_pct', models.FloatField(blank=True, db_column='FG3_PCT', null=True)),
                ('ftm', models.IntegerField(blank=True, db_column='FTM', null=True)),
                ('fta', models.IntegerField(blank=True, db_column='FTA', null=True)),
                ('ft_pct', models.FloatField(blank=True, db_column='FT_PCT', null=True)),
                ('oreb', models.IntegerField(blank=True, db_column='OREB', null=True)),
                ('dreb', models.IntegerField(blank=True, db_column='DREB', null=True)),
                ('reb', models.IntegerField(blank=True, db_column='REB', null=True)),
                ('ast', models.IntegerField(blank=True, db_column='AST', null=True)),
                ('stl', models.IntegerField(blank=True, db_column='STL', null=True)),
                ('blk', models.IntegerField(blank=True, db_column='BLK', null=True)),
                ('tov', models.IntegerField(blank=True, db_column='TOV', null=True)),
                ('pf', models.IntegerField(blank=True, db_column='PF', null=True)),
                ('pts', models.IntegerField(blank=True, db_column='PTS', null=True)),
            ],
            options={
                'db_table': 'Stats',
                'managed': False,
            },
        ),
    ]