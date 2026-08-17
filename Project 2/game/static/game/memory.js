const EMOJIS = ["🍎", "🍌", "🍇", "🍓", "🍒", "🍉", "🥝", "🍍"];

const board = document.getElementById("board");
const movesEl = document.getElementById("moves");
const pairsEl = document.getElementById("pairs");
const timerEl = document.getElementById("timer");
const modal = document.getElementById("win-modal");
const winMovesEl = document.getElementById("win-moves");
const winTimeEl = document.getElementById("win-time");
const movesInput = document.getElementById("win-moves-input");
const secondsInput = document.getElementById("win-seconds-input");

let cards = [];
let first = null;
let lock = false;
let moves = 0;
let pairsFound = 0;
let seconds = 0;
let timerId = null;

function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function formatTime(total) {
    const m = Math.floor(total / 60);
    const s = total % 60;
    return `${m}:${String(s).padStart(2, "0")}`;
}

function buildDeck() {
    return shuffle([...EMOJIS, ...EMOJIS]);
}

function render() {
    board.innerHTML = "";
    cards.forEach((emoji, i) => {
        const card = document.createElement("div");
        card.className = "card";
        card.dataset.index = i;
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-face card-front">${emoji}</div>
                <div class="card-face card-back"></div>
            </div>`;
        card.addEventListener("click", () => flip(i));
        board.appendChild(card);
    });
}

function startTimer() {
    if (timerId) return;
    timerId = setInterval(() => {
        seconds++;
        timerEl.textContent = formatTime(seconds);
    }, 1000);
}

function flip(i) {
    const card = board.children[i];
    if (lock || card.classList.contains("flipped") || card.classList.contains("matched")) return;

    card.classList.add("flipped");
    if (first === null) {
        first = i;
        return;
    }

    moves++;
    movesEl.textContent = moves;

    if (cards[first] === cards[i]) {
        board.children[first].classList.add("matched", "locked");
        card.classList.add("matched", "locked");
        first = null;
        pairsFound++;
        pairsEl.textContent = pairsFound;
        if (pairsFound === EMOJIS.length) win();
    } else {
        lock = true;
        const prev = first;
        first = null;
        setTimeout(() => {
            board.children[prev].classList.remove("flipped");
            card.classList.remove("flipped");
            lock = false;
        }, 800);
    }
}

function win() {
    clearInterval(timerId);
    timerId = null;
    winMovesEl.textContent = moves;
    winTimeEl.textContent = formatTime(seconds);
    movesInput.value = moves;
    secondsInput.value = seconds;
    modal.classList.remove("hidden");
}

function restart() {
    clearInterval(timerId);
    timerId = null;
    first = null;
    lock = false;
    moves = 0;
    pairsFound = 0;
    seconds = 0;
    movesEl.textContent = "0";
    pairsEl.textContent = "0";
    timerEl.textContent = "0:00";
    modal.classList.add("hidden");
    cards = buildDeck();
    render();
    startTimer();
}

document.getElementById("restart").addEventListener("click", restart);

restart();