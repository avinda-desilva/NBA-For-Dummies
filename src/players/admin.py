from django.contrib import admin

from django.contrib import admin

# Register your models here.

from .models import Players, UserPlayers, User2



#@admin.register(Players)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("player_id", "season_id", "team_id", "player_name", "points")

class UserPlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "player_id", "season_id", "team_id", "player_name", "points")

class User2Admin(admin.ModelAdmin):
    list_display = ("id", "player_id", "season_id", "team_id", "player_name", "points")

admin.site.register(Players, PlayerAdmin)
admin.site.register(UserPlayers, UserPlayerAdmin)
admin.site.register(User2, User2Admin)


#class PlayerAdmin(ImportExportModelAdmin):
#    pass
