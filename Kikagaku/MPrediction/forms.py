from django import forms
from MPrediction.models import Team, Player, Membership, SeasonResult


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'team_no']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'team', 'player_no', 'birth']
        widgets = {'birth': forms.DateInput(attrs={'type': 'date'})}

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['player', 'team', 'year', 'player_age', 'player_career', 'player_titles']

class SeasonResultForm(forms.ModelForm):
    class Meta:
        model = SeasonResult
        fields = [
            'membership', 'stage', 'games', 'hands', 'points', 'first_place', 
            'second_place', 'third_place', 'last_place', 'high_score', 'average_score',
            'average_score_lost', 'mangan_or_higher_rate', 'win_hand_rate', 'dealin_rate',
            'riichi_declaration_rate','call_rate', 'tenpai_rate_at_exhaustive_draw',
            'tenpai_bounus_net_gain_at_draw', 'draw_rate'
            ]