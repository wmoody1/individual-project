from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Week(models.Model)
#    week_number = models.IntegerField()

class Game(models.Model):
    favorite = models.CharField(max_length=200)
    underdog = models.CharField(max_length=200)
    line = models.DecimalField(decimal_places=1, max_digits=3)
    tv = models.CharField(max_length=20)
    datetime = models.DateTimeField(default=0)
    week = models.IntegerField(default=0)
    game_of_the_week = models.BooleanField(default=False)
    game_winner = models.NullBooleanField()

    def __str__(self):
        return self.favorite + ' vs ' + self.underdog


class Bet(models.Model):
    # participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    # game = models.ForeignKey('Game', on_delete=models.CASCADE)

    userID = models.IntegerField(default=0)
    gameID = models.IntegerField(default=0)
    week = models.IntegerField(default=0)
    winner = models.BooleanField()
    is_valid = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("userID", "gameID")

    def __str__(self):
        u = User.objects.get(id=self.userID)
        name = u.first_name
        if name == "":
            name = u.username
        return "Bet for User: " + name + "; Game: " + str(self.gameID)


class Setting(models.Model):
    setting = models.CharField(max_length=500, unique=True)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.setting + ": " + self.value


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bet = models.ManyToManyField('Bet')
    total_points = models.IntegerField(default=0)
    has_paid = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Participant.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.participant.save()


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' score for Week: ' + self.week.value_to_string


class GameOfWeekScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
