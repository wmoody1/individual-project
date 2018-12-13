from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.db import connection

from .models import Game, Bet, Setting, Participant, GameOfWeekScore
from .functions import predict_participant_score

def sheet(request):
    current_week = Setting.objects.get(setting="CurrentWeek")
    user_id = request.user.id
    current_week_game_list = Game.objects.filter(week=current_week.value).order_by('id')
    current_user_bets = Bet.objects.filter(userID=user_id, week=current_week.value)

    game_of_the_week = Game.objects.filter(week=current_week.value, game_of_the_week=True)

    if request.method == "POST":
        user_id = request.POST["userID"]
        game_of_the_week_points = request.POST["game_of_the_week_points"]

        for game in current_week_game_list:
            if "g" + str(game.id) in request.POST:
                selection = request.POST["g" + str(game.id)]
                if selection == game.favorite:
                    winner = True
                else:
                    winner = False
                try:
                    select_object = Bet.objects.get(userID=user_id, gameID=game.id)
                    if "submit_sheet" in request.POST:
                        b = Bet(id=select_object.id, userID=user_id, gameID=game.id, week=current_week.value,
                                winner=winner, game=game, is_valid=True)
                    else:
                        b = Bet(id=select_object.id, userID=user_id, gameID=game.id, week=current_week.value,
                                winner=winner, game=game, is_valid=False)
                    b.save()
                except Bet.DoesNotExist:
                    if "submit_sheet" in request.POST:
                        b = Bet(userID=user_id, gameID=game.id, week=current_week.value,
                                winner=winner, game=game, is_valid=True)
                    else:
                        b = Bet(userID=user_id, gameID=game.id, week=current_week.value,
                                winner=winner, game=game, is_valid=False)
                    b.save()

        if game_of_the_week_points in request.POST:
            try:
                game_of_week_score_object = GameOfWeekScore.objects.get(user=request.user, week=current_week.value)
                game_of_week_score_object.score = game_of_the_week_points
                game_of_week_score_object.save()
            except GameOfWeekScore.DoesNotExist:
                game_of_week_score = GameOfWeekScore(user=request.user, week=current_week.value,
                                                     score=game_of_the_week_points)
                game_of_week_score.save()

    cursor = connection.cursor()
    cursor.execute("""
                    SELECT g.*, b.winner
                    FROM collegebettingpoolapp_game g 
                    LEFT JOIN collegebettingpoolapp_bet b
                        ON b.gameID = g.id
                    WHERE g.week = %s
                        AND (b.userID = %s
                                OR b.userID IS NULL)
                    ORDER BY g.id ASC
                                """, [current_week.value, user_id])

    query = cursor.fetchall()

    context = {'current_week_game_list': current_week_game_list,
               'game_of_the_week': game_of_the_week,
               'current_user_bets': current_user_bets,
               'query': query}

    return render(request, 'collegebettingpoolapp/sheet.html', context)


def scores(request):
    try:
        participants = Participant.objects.all().order_by('-total_points')
    except (KeyError, Participant.DoesNotExist):
        participants = ['null msg', 'null msg']

    context = {'participants': participants}

    return render(request, 'collegebettingpoolapp/scores.html', context)


def history(request):
    current_week = Setting.objects.get(setting="CurrentWeek")
    user_id = request.user.id

    current_week_game_list = Game.objects.all().filter(week=current_week.value).order_by('id')

    current_user_bets = Bet.objects.all().filter(week=current_week.value, userID=user_id)

    cursor = connection.cursor()
    cursor.execute("""
                        SELECT g.*, b.winner
                        FROM collegebettingpoolapp_game g 
                        LEFT JOIN collegebettingpoolapp_bet b
                            ON b.gameID = g.id
                        WHERE g.week <> %s
                            AND (b.userID = %s
                                    OR b.userID IS NULL)
                        ORDER BY g.week ASC, g.id ASC
                                    """, [current_week.value, user_id])

    query = cursor.fetchall()

    context = {'current_week_game_list': current_week_game_list,
               'query': query,
               'weeks': range(1, int(current_week.value))}

    return render(request, 'collegebettingpoolapp/history.html', context)


def closeout(request):
    current_week = Setting.objects.get(setting="CurrentWeek")

    if request.method == "POST":
        participant_list = Participant.objects.all()
        running_score = 0

        for p in participant_list:
            p_id = p.user.id
            bets = Bet.objects.filter(userID=p_id, week=current_week.value, is_valid=True)

            score, games_won = predict_participant_score(bet_list=bets)
            running_score += score

            p.total_points += score
            p.save()

        new_week = int(current_week.value) + 1
        current_week.value = new_week
        current_week.save()

    participant_list = Participant.objects.all()
    running_score = 0

    for p in participant_list:
        p_id = p.user.id
        bets = Bet.objects.filter(userID=p_id, week=current_week.value, is_valid=True)

        score, games_won = predict_participant_score(bet_list=bets)
        running_score += score

    context = {'current_week': int(current_week.value),
               'running_score': running_score,
               'participants': participant_list}

    return render(request, 'collegebettingpoolapp/closeout.html', context)


def about(request):
    return render(request, 'collegebettingpoolapp/about.html')


def index(request):
    return render(request, 'collegebettingpoolapp/home.html')
