from django.contrib import admin
from .models import Game, Bet, Setting, GameOfWeekScore, Participant

# def close_out_week(modeladmin, request, queryset):
# 	for Game in queryset:
# 		game_list = Game.objects.filter(week=current_week)
# 		for game in game_list:
# 			bet_list = game.bet_set.all()
# 			bet_list = Bet.objects.all().filter(game=Game)
# 			for bet in bet_list:
# 				if bet.winner==:
# 					#if bet.is_high_risk_game:
# 					#	bet.user.total_points+=5
# 					#else if bet.is_game_of_the_week:
# 					#	bet.user.total_points+=2
# 					#else:
# 					bet.user.total_points+=1
# 				else:
# 					#if bet.is_high_risk_game:
# 					#	bet.user.total_points-=5
# 					#else if bet.is_game_of_the_week:
# 					#	bet.user.total_points-=2
# 					#else:
# 					bet.user.total_points-=1

# class GameAdmin(admin.ModelAdmin):
# 	list_display = ['favorite', 'week']
# 	ordering = ['week']
# 	actions = [close_out_week]


# Register your models here.
admin.site.register(Game)
admin.site.register(Bet)
admin.site.register(Setting)
admin.site.register(GameOfWeekScore)
admin.site.register(Participant)
