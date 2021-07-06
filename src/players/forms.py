from django import forms
from .models import Players, Stats, UserPlayers, User2, User2Stats, User1Stats

class UserForm2(forms.ModelForm):
    class Meta:
        model = User2Stats
        fields = '__all__'

class UserForm1(forms.ModelForm):
    class Meta:
        model = User1Stats
        fields = '__all__'

class StatsForm(forms.ModelForm):
    class Meta:
        model = Stats
        fields = ['pts']

class PlayersForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['player_id','season_id','team_id','player_name','points']
        widgets = {'team_id' : forms.TextInput}


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['player_id','season_id','team_id','player_name','points']
        widgets = {'team_id' : forms.TextInput}

class DeleteForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['season_id','player_name','points']
#        widgets = {'team_id' : forms.TextInput}

#        def valid_update(self):
#            p_name = self.cleaned_data.get('player_name')
#            team_id = self.cleaned_data.get('team_id')
#            season_id = self.cleaned_data.get('season_id')
#            player_id = self.cleaned_data.get('player_id')
#            new_points = self.cleaned_data.get('points')
#            object_list = Players.objects.raw('SELECT * FROM Player WHERE player_id = %s AND season_id = %s AND team_id = %s', [player_id, season_id, team_id]).update(points=new_points)
#            print(object_list[0].points)
