from django.contrib import admin
from .models import CakeBase, Frosting, Topping, HighScore

admin.site.register(CakeBase)
admin.site.register(Frosting)
admin.site.register(Topping)
admin.site.register(HighScore)
