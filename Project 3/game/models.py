from django.db import models


class CakeBase(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, help_text="CSS color for the cake body")

    def __str__(self):
        return self.name


class Frosting(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, help_text="CSS color for the frosting layer")

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=50)
    emoji = models.CharField(max_length=10)
    points = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name


class HighScore(models.Model):
    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField()
    toppings_used = models.PositiveIntegerField(default=0)
    time_taken = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.name}: {self.score}"
