from django.core.management.base import BaseCommand
from game.models import CakeBase, Frosting, Topping


class Command(BaseCommand):
    help = "Seed the game with cake bases, frostings and toppings"

    def handle(self, *args, **options):
        bases = [
            ("Vanilla Sponge", "#f7e8c9"),
            ("Chocolate Sponge", "#7b4a2d"),
            ("Strawberry Sponge", "#f7c8d4"),
        ]
        frostings = [
            ("Creamy White", "#fff8f0"),
            ("Pink Buttercream", "#f8b6c9"),
            ("Chocolate Ganache", "#5a3a22"),
            ("Mint Frosting", "#c9f0dc"),
        ]
        toppings = [
            ("Cherry", "🍒", 10),
            ("Sprinkles", "🌈", 10),
            ("Candle", "🕯️", 15),
            ("Strawberry", "🍓", 10),
            ("Blueberry", "🫐", 10),
            ("Chocolate Chip", "🍫", 10),
            ("Flower", "🌸", 15),
            ("Berry", "🍇", 10),
        ]

        for name, color in bases:
            CakeBase.objects.get_or_create(name=name, defaults={"color": color})
        for name, color in frostings:
            Frosting.objects.get_or_create(name=name, defaults={"color": color})
        for name, emoji, points in toppings:
            Topping.objects.get_or_create(name=name, defaults={"emoji": emoji, "points": points})

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {CakeBase.objects.count()} bases, "
            f"{Frosting.objects.count()} frostings, "
            f"{Topping.objects.count()} toppings"
        ))