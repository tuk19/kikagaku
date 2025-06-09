from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    team_no = models.IntegerField(unique=True)

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    player_no = models.IntegerField(unique=True)
    birth = models.DateField(null=True, blank=True)


class Membership(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.IntegerField()
    player_age = models.IntegerField(null=True, blank=True)
    player_career = models.IntegerField(null=True, blank=True)
    player_titles = models.IntegerField(null=True, blank=True)


class SeasonResult(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20)
    games = models.IntegerField(null=True, blank=True)
    hands = models.IntegerField(null=True, blank=True)
    points = models.FloatField(null=True, blank=True)
    first_place = models.IntegerField(null=True, blank=True)
    second_place = models.IntegerField(null=True, blank=True)
    third_place = models.IntegerField(null=True, blank=True)
    last_place = models.IntegerField(null=True, blank=True)
    high_score = models.IntegerField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)
    average_score_lost = models.FloatField(null=True, blank=True)
    mangan_or_higher_rate = models.FloatField(null=True, blank=True)
    win_hand_rate = models.FloatField(null=True, blank=True)
    dealin_rate = models.FloatField(null=True, blank=True)
    riichi_declaration_rate = models.FloatField(null=True, blank=True)
    call_rate = models.FloatField(null=True, blank=True)
    tenpai_rate_at_exhaustive_draw = models.FloatField(null=True, blank=True)
    tenpai_bounus_net_gain_at_draw = models.FloatField(null=True, blank=True)
    draw_rate = models.FloatField(null=True, blank=True)
    