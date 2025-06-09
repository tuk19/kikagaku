from django.shortcuts import render, redirect
from MPrediction.models import Team, Player, Membership, SeasonResult
from MPrediction.forms import TeamForm, PlayerForm, MembershipForm, SeasonResultForm


def index(request):
    return render(request, 'mprediction/index.html')

def team(request):
    team = Team.objects.all()
    context = {
        'title': 'チーム',
        'data': team,
    }
    return render(request, 'mprediction/team.html', context)

def team_create(request):
    if request.method == 'POST':
        obj = Team()
        team = TeamForm(request.POST, instance=obj)
        team.save()
        return redirect(to='mprediction:team')
    context = {
        'title': 'チーム追加',
        'form': TeamForm()
    }
    return render(request, 'mprediction/team_create.html', context)

def team_edit(request, num):
    obj = Team.objects.get(id=num)
    if request.method == 'POST':
        team = TeamForm(request.POST, instance=obj)
        team.save()
        return redirect(to='mprediction:team')
    context = {
        'title': 'チーム修正',
        'id': num,
        'form': TeamForm(instance=obj)
    }
    return render(request, 'mprediction/team_edit.html', context)

def player(request):
    player = Player.objects.all()
    context = {
        'title': '選手',
        'data': player,
    }
    return render(request, 'mprediction/player.html', context)

def player_create(request):
    if request.method == 'POST':
        obj = Player()
        player = PlayerForm(request.POST, instance=obj)
        player.save()
        return redirect(to='mprediction:player')
    context = {
        'title': '選手追加',
        'form': PlayerForm()
    }
    return render(request, 'mprediction/player_create.html', context)

def player_edit(request, num):
    obj = Player.objects.get(id=num)
    if request.method == 'POST':
        player = PlayerForm(request.POST, instance=obj)
        player.save()
        return redirect(to='mprediction:player')
    context = {
        'title': '選手修正',
        'id': num,
        'form': PlayerForm(instance=obj)
    }
    return render(request, 'mprediction/player_edit.html', context)

def member(request):
    member = Membership.objects.all()
    context = {
        'title': '選手',
        'data': member,
    }
    return render(request, 'mprediction/member.html', context)

def member_create(request):
    if request.method == 'POST':
        obj = Membership()
        member = MembershipForm(request.POST, instance=obj)
        member.save()
        return redirect(to='mprediction:member')
    context = {
        'title': '選手追加',
        'form': MembershipForm()
    }
    return render(request, 'mprediction/member_create.html', context)

def member_edit(request, num):
    obj = Membership.objects.get(id=num)
    if request.method == 'POST':
        member = MembershipForm(request.POST, instance=obj)
        member.save()
        return redirect(to='mprediction:member')
    context = {
        'title': '選手修正',
        'id': num,
        'form': MembershipForm(instance=obj)
    }
    return render(request, 'mprediction/member_edit.html', context)

def season(request):
    season = SeasonResult.objects.all()
    context = {
        'title': 'チーム',
        'data': season,
    }
    return render(request, 'mprediction/season.html', context)

def season_create(request):
    if request.method == 'POST':
        obj = SeasonResult()
        season = SeasonResultForm(request.POST, instance=obj)
        season.save()
        return redirect(to='mprediction:season')
    context = {
        'title': 'チーム追加',
        'form': SeasonResultForm()
    }
    return render(request, 'mprediction/season_create.html', context)

def season_edit(request, num):
    obj = SeasonResult.objects.get(id=num)
    if request.method == 'POST':
        season = SeasonResultForm(request.POST, instance=obj)
        season.save()
        return redirect(to='mprediction:season')
    context = {
        'title': 'チーム修正',
        'id': num,
        'form': SeasonResultForm(instance=obj)
    }
    return render(request, 'mprediction/season_edit.html', context)