from .models import Game


def predict_participant_score(bet_list):
    points_to_add = 0
    games_won = 0
    for bet in bet_list:
        game = Game.objects.get(id=bet.gameID)

        if bet.winner == game.game_winner:
            points_to_add += 1
            games_won += 1

            if game.game_of_the_week:
                points_to_add += 2

    return points_to_add, games_won
