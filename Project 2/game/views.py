from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Score


def board(request):
    best = Score.objects.first()
    return render(request, "game/board.html", {"best": best})


@require_POST
def save_score(request):
    player = request.POST.get("player", "").strip()[:50] or "Anonymous"
    try:
        moves = int(request.POST.get("moves"))
        seconds = int(request.POST.get("seconds"))
    except (TypeError, ValueError):
        return redirect("game:board")
    if moves < 1 or seconds < 0:
        return redirect("game:board")
    Score.objects.create(player=player, moves=moves, seconds=seconds)
    return redirect("game:high_scores")


def high_scores(request):
    scores = Score.objects.all()[:10]
    return render(request, "game/high_scores.html", {"scores": scores})