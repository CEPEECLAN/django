from django.db import models


class SteamUser(models.Model):
    steamid = models.IntegerField()
    personaname = models.TextField()
    avatar_url = models.TextField()
    stats = models.TextField()
    achievements = models.TextField()

