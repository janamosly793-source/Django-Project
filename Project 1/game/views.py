import random

from django.shortcuts import redirect, render


def index(request):
    if "secret" not in request.session:
        request.session["secret"] = random.randint(1, 100)
        request.session["attempts"] = 0
        request.session["history"] = []

    context = {
        "attempts": request.session["attempts"],
        "history": request.session["history"],
    }

    if request.method == "POST":
        guess = request.POST.get("guess", "").strip()
        context["guess"] = guess

        if not guess.isdigit() or not 1 <= int(guess) <= 100:
            context["message"] = "Please enter a number between 1 and 100."
            return render(request, "game/index.html", context)

        guess = int(guess)
        secret = request.session["secret"]
        request.session["attempts"] += 1
        request.session["history"].append(guess)

        if guess == secret:
            context["message"] = (
                f"Correct! You guessed {secret} in "
                f"{request.session['attempts']} attempts."
            )
            context["won"] = True
        elif guess < secret:
            context["message"] = "Too low! Try a higher number."
        else:
            context["message"] = "Too high! Try a lower number."

        request.session.modified = True
        context["attempts"] = request.session["attempts"]

    return render(request, "game/index.html", context)


def reset(request):
    request.session.flush()
    return redirect("index")