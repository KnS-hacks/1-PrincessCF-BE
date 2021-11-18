from django.db import models

# Create your models here.

class Music(models.Model):
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    is_not_played = models.BooleanField(default=True)

    def __str__(self):
        return self.artist + " - " + self.title