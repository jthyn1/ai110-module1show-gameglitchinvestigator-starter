# FIX: Core game logic refactored out of app.py into this module with Claude Code
# (agent mode), so it can be unit tested without running Streamlit.

HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    # FIX: Messages were swapped in the original code ("Too High" said "Go HIGHER!").
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard used to be 1-50, which made it easier than Normal (1-100).
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If low/high are given, guesses outside that inclusive range are rejected.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    # FIX: Decimals like "3.9" were silently truncated to 3; now they are rejected.
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "That is not a whole number."

    # FIX: Out-of-range guesses (e.g. -5 or 500) used to be accepted and cost an attempt.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: Always compare ints. The original app turned the secret into a str on
    # even attempts, so comparisons became alphabetical (e.g. 9 > "50").
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str):
    """Return the hint text shown to the player for an outcome."""
    return HINT_MESSAGES[outcome]


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number (1 = first guess).

    A win is worth 100 on the first guess, 10 fewer for each extra guess
    (minimum 10). Every wrong guess costs 5 points.
    """
    if outcome == "Win":
        # FIX: Was 100 - 10 * (attempt_number + 1), so a first-try win only scored 80.
        points = max(100 - 10 * (attempt_number - 1), 10)
        return current_score + points

    # FIX: "Too High" used to award +5 on even attempts; wrong guesses now always cost 5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
