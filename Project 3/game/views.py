import random

from django.shortcuts import render, redirect

from .models import CakeBase, Frosting, Topping, HighScore

TIME_LIMIT = 60


def _new_order():
    bases = list(CakeBase.objects.all())
    frostings = list(Frosting.objects.all())
    toppings = list(Topping.objects.all())
    if not bases or not frostings or not toppings:
        return None
    needed = random.sample(toppings, min(4, len(toppings)))
    return {
        "base_id": random.choice(bases).id,
        "frosting_id": random.choice(frostings).id,
        "needed_ids": [t.id for t in needed],
        "wrong_ids": [t.id for t in toppings if t.id not in [n.id for n in needed]],
    }


def menu(request):
    return render(request, "game/menu.html")


def play(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "reset":
            request.session.pop("order", None)
            request.session.pop("decorated", None)
            return redirect("play")
        if action == "add_topping":
            topping_id = int(request.POST.get("topping_id"))
            decorated = request.session.get("decorated", [])
            if topping_id not in decorated:
                decorated.append(topping_id)
                request.session["decorated"] = decorated
        elif action == "finish":
            order = request.session.get("order")
            decorated = request.session.get("decorated", [])
            if order:
                return _finish(request, order, decorated)

    if "order" not in request.session:
        request.session["order"] = _new_order()
        request.session["decorated"] = []

    order = request.session["order"]
    decorated = request.session.get("decorated", [])

    if order is None:
        return render(
            request, "game/play.html",
            {"error": "No cake data available. Add bases, frostings and toppings in admin first."},
        )

    bases = CakeBase.objects.all()
    frostings = Frosting.objects.all()
    toppings = Topping.objects.all()
    needed_toppings = Topping.objects.filter(id__in=order["needed_ids"])

    context = {
        "order": order,
        "bases": bases,
        "frostings": frostings,
        "toppings": toppings,
        "needed_toppings": needed_toppings,
        "decorated": decorated,
        "time_limit": TIME_LIMIT,
    }
    return render(request, "game/play.html", context)


def _finish(request, order, decorated):
    base = CakeBase.objects.get(id=order["base_id"])
    frosting = Frosting.objects.get(id=order["frosting_id"])
    chosen_base = int(request.POST.get("base_id", 0))
    chosen_frosting = int(request.POST.get("frosting_id", 0))

    score = 0
    details = []
    if chosen_base == base.id:
        score += 30
        details.append(f"Base: {base.name} (30 pts)")
    else:
        details.append("Base: wrong (0 pts)")
    if chosen_frosting == frosting.id:
        score += 30
        details.append(f"Frosting: {frosting.name} (30 pts)")
    else:
        details.append("Frosting: wrong (0 pts)")

    for t in Topping.objects.filter(id__in=order["needed_ids"]):
        if t.id in decorated:
            score += t.points
            details.append(f"Topping: {t.name} (+{t.points})")
    for t in Topping.objects.filter(id__in=order["wrong_ids"]):
        if t.id in decorated:
            score -= 5
            details.append(f"Topping: {t.name} (-5, not on order)")

    time_taken = int(request.POST.get("time_taken", TIME_LIMIT))
    time_bonus = max(0, TIME_LIMIT - time_taken)
    score += time_bonus
    details.append(f"Time bonus: +{time_bonus}")

    request.session["result"] = {
        "score": score,
        "details": details,
        "toppings_used": len(decorated),
        "time_taken": time_taken,
        "base_name": base.name,
        "frosting_name": frosting.name,
        "base_id": chosen_base,
        "frosting_id": chosen_frosting,
        "decorated": decorated,
    }
    request.session.pop("order", None)
    request.session.pop("decorated", None)
    return redirect("result")


def result(request):
    result = request.session.get("result")
    if not result:
        return redirect("play")

    name = ""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()[:50]
        if name:
            HighScore.objects.create(
                name=name,
                score=result["score"],
                toppings_used=result["toppings_used"],
                time_taken=result["time_taken"],
            )
            request.session.pop("result", None)
            return redirect("scores")

    return render(request, "game/result.html", {"result": result, "name": name})


def scores(request):
    scores = HighScore.objects.all()[:10]
    return render(request, "game/scores.html", {"scores": scores})