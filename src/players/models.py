from django.db import models

# Create your models here.


#class Players(models.Model):
#    name = models.CharField(max_length=255)
#    team = models.CharField(max_length=255)
#    class Meta:
#        verbose_name = "players"
#    def __str__(self):
#        return self.name

class SearchPlayers(models.Model):
#    table_id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(primary_key=True)
    season_id = models.CharField(max_length=10)
    team_id = models.IntegerField()
    player_name = models.CharField(max_length=30)
    points = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Player'
        unique_together = (('player_id', 'season_id', 'team_id'),)


class UserPlayers(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    season_id = models.CharField(max_length=45, blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    player_name = models.CharField(max_length=45, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'

class User2(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    season_id = models.CharField(max_length=45, blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    player_name = models.CharField(max_length=45, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User2'

# class UserPlayers(models.Model):
#     id = models.IntegerField(primary_key=True)
#     player_id = models.IntegerField(primary_key=True)
#     season_id = models.CharField(max_length=10)
#     team_id = models.IntegerField()
#     player_name = models.CharField(max_length=30)
#     points = models.IntegerField()
#
#     # @classmethod
#     # def create(cls, pk):
#     #     user_player = cls()
#     #     return user_player
#
#     class Meta:
#         managed = False
#         db_table = 'User'
        # unique_together = (('player_id', 'season_id', 'team_id'),)


class Players(models.Model):
    # table_id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(primary_key=True)
    season_id = models.CharField(max_length=10)
    team_id = models.IntegerField()
    player_name = models.CharField(max_length=30)
    points = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Player'
        unique_together = (('player_id', 'season_id', 'team_id'),)

class Teams(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    team_name = models.CharField(max_length=30)
    year_founded = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Teams'

class Stats(models.Model):
    player_id = models.IntegerField(primary_key=True)
    season_id = models.CharField(max_length=10)
    league_id = models.IntegerField()
    team_id = models.IntegerField()
    team_abbr = models.CharField(max_length=10)
    age = models.IntegerField()
    gp = models.IntegerField(db_column='GP', blank=True, null=True)  # Field name made lowercase.
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  # Field name made lowercase.
    min = models.IntegerField(db_column='MIN', blank=True, null=True)  # Field name made lowercase.
    fgm = models.IntegerField(db_column='FGM', blank=True, null=True)  # Field name made lowercase.
    fga = models.IntegerField(db_column='FGA', blank=True, null=True)  # Field name made lowercase.
    fg_pct = models.FloatField(db_column='FG_PCT', blank=True, null=True)  # Field name made lowercase.
    fg3m = models.IntegerField(db_column='FG3M', blank=True, null=True)  # Field name made lowercase.
    fg3a = models.IntegerField(db_column='FG3A', blank=True, null=True)  # Field name made lowercase.
    fg3_pct = models.FloatField(db_column='FG3_PCT', blank=True, null=True)  # Field name made lowercase.
    ftm = models.IntegerField(db_column='FTM', blank=True, null=True)  # Field name made lowercase.
    fta = models.IntegerField(db_column='FTA', blank=True, null=True)  # Field name made lowercase.
    ft_pct = models.FloatField(db_column='FT_PCT', blank=True, null=True)  # Field name made lowercase.
    oreb = models.IntegerField(db_column='OREB', blank=True, null=True)  # Field name made lowercase.
    dreb = models.IntegerField(db_column='DREB', blank=True, null=True)  # Field name made lowercase.
    reb = models.IntegerField(db_column='REB', blank=True, null=True)  # Field name made lowercase.
    ast = models.IntegerField(db_column='AST', blank=True, null=True)  # Field name made lowercase.
    stl = models.IntegerField(db_column='STL', blank=True, null=True)  # Field name made lowercase.
    blk = models.IntegerField(db_column='BLK', blank=True, null=True)  # Field name made lowercase.
    tov = models.IntegerField(db_column='TOV', blank=True, null=True)  # Field name made lowercase.
    pf = models.IntegerField(db_column='PF', blank=True, null=True)  # Field name made lowercase.
    pts = models.IntegerField(db_column='PTS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stats'
        unique_together = (('player_id', 'season_id', 'team_id'),)


class User1Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    player_name = models.CharField(max_length=45, blank=True, null=True)
    season_id = models.CharField(max_length=45, blank=True, null=True)
    league_id = models.IntegerField(blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    team_abbr = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gp = models.IntegerField(db_column='GP', blank=True, null=True)  # Field name made lowercase.
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  # Field name made lowercase.
    min = models.IntegerField(db_column='MIN', blank=True, null=True)  # Field name made lowercase.
    fgm = models.IntegerField(db_column='FGM', blank=True, null=True)  # Field name made lowercase.
    fga = models.IntegerField(db_column='FGA', blank=True, null=True)  # Field name made lowercase.
    fg_pct = models.DecimalField(db_column='FG_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fg3m = models.IntegerField(db_column='FG3M', blank=True, null=True)  # Field name made lowercase.
    fg3a = models.IntegerField(db_column='FG3A', blank=True, null=True)  # Field name made lowercase.
    fg3_pct = models.DecimalField(db_column='FG3_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ftm = models.IntegerField(db_column='FTM', blank=True, null=True)  # Field name made lowercase.
    fta = models.IntegerField(db_column='FTA', blank=True, null=True)  # Field name made lowercase.
    ft_pct = models.DecimalField(db_column='FT_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    oreb = models.IntegerField(db_column='OREB', blank=True, null=True)  # Field name made lowercase.
    dreb = models.IntegerField(db_column='DREB', blank=True, null=True)  # Field name made lowercase.
    reb = models.IntegerField(db_column='REB', blank=True, null=True)  # Field name made lowercase.
    ast = models.IntegerField(db_column='AST', blank=True, null=True)  # Field name made lowercase.
    stl = models.IntegerField(db_column='STL', blank=True, null=True)  # Field name made lowercase.
    blk = models.IntegerField(db_column='BLK', blank=True, null=True)  # Field name made lowercase.
    tov = models.IntegerField(db_column='TOV', blank=True, null=True)  # Field name made lowercase.
    pf = models.IntegerField(db_column='PF', blank=True, null=True)  # Field name made lowercase.
    pts = models.IntegerField(db_column='PTS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user1stats'


class User2Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    player_id = models.IntegerField(blank=True, null=True)
    player_name = models.CharField(max_length=45, blank=True, null=True)
    season_id = models.CharField(max_length=45, blank=True, null=True)
    league_id = models.IntegerField(blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    team_abbr = models.CharField(max_length=45, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gp = models.IntegerField(db_column='GP', blank=True, null=True)  # Field name made lowercase.
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  # Field name made lowercase.
    min = models.IntegerField(db_column='MIN', blank=True, null=True)  # Field name made lowercase.
    fgm = models.IntegerField(db_column='FGM', blank=True, null=True)  # Field name made lowercase.
    fga = models.IntegerField(db_column='FGA', blank=True, null=True)  # Field name made lowercase.
    fg_pct = models.DecimalField(db_column='FG_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    fg3m = models.IntegerField(db_column='FG3M', blank=True, null=True)  # Field name made lowercase.
    fg3a = models.IntegerField(db_column='FG3A', blank=True, null=True)  # Field name made lowercase.
    fg3_pct = models.DecimalField(db_column='FG3_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ftm = models.IntegerField(db_column='FTM', blank=True, null=True)  # Field name made lowercase.
    fta = models.IntegerField(db_column='FTA', blank=True, null=True)  # Field name made lowercase.
    ft_pct = models.DecimalField(db_column='FT_PCT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    oreb = models.IntegerField(db_column='OREB', blank=True, null=True)  # Field name made lowercase.
    dreb = models.IntegerField(db_column='DREB', blank=True, null=True)  # Field name made lowercase.
    reb = models.IntegerField(db_column='REB', blank=True, null=True)  # Field name made lowercase.
    ast = models.IntegerField(db_column='AST', blank=True, null=True)  # Field name made lowercase.
    stl = models.IntegerField(db_column='STL', blank=True, null=True)  # Field name made lowercase.
    blk = models.IntegerField(db_column='BLK', blank=True, null=True)  # Field name made lowercase.
    tov = models.IntegerField(db_column='TOV', blank=True, null=True)  # Field name made lowercase.
    pf = models.IntegerField(db_column='PF', blank=True, null=True)  # Field name made lowercase.
    pts = models.IntegerField(db_column='PTS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user2stats'
