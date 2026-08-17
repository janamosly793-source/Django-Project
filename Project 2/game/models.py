from django.db import models


class Score(models.Model):
    player = models.CharField(max_length=50)
    moves = models.PositiveIntegerField()
    seconds = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["moves", "seconds"]

    def __str__(self):
        return f"{self.player} - {self.moves} moves"