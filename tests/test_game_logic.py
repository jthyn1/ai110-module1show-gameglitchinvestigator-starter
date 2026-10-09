from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Regression tests for bugs fixed with Claude Code ---

from logic_utils import get_hint_message, get_range_for_difficulty, parse_guess, update_score


def test_too_high_hint_says_go_lower():
    # Bug: guessing 60 against 50 told the player to go HIGHER
    assert "LOWER" in get_hint_message(check_guess(60, 50))


def test_too_low_hint_says_go_higher():
    assert "HIGHER" in get_hint_message(check_guess(40, 50))


def test_single_digit_guess_vs_two_digit_secret():
    # Bug: secret became a str on even attempts, so 9 vs "50" compared as text
    # and said "Too High". With ints, 9 is lower than 50.
    assert check_guess(9, 50) == "Too Low"


def test_hard_range_is_wider_than_normal():
    # Bug: Hard was 1-50, narrower (easier) than Normal's 1-100
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_first_try_win_scores_100():
    # Bug: first-try win only scored 80
    assert update_score(0, "Win", 1) == 100


def test_too_high_never_adds_points():
    # Bug: a "Too High" guess on an even attempt added 5 points
    assert update_score(0, "Too High", 2) == -5


# --- Edge cases (Challenge 1) ---

def test_negative_guess_rejected():
    ok, value, err = parse_guess("-5", 1, 20)
    assert not ok and value is None and err


def test_decimal_guess_rejected():
    # Used to be silently truncated: "3.9" became 3
    ok, value, _ = parse_guess("3.9", 1, 20)
    assert not ok and value is None


def test_huge_guess_rejected():
    ok, _, _ = parse_guess("99999999999999999999", 1, 100)
    assert not ok


def test_guess_with_spaces_accepted():
    assert parse_guess(" 42 ", 1, 100) == (True, 42, None)


def test_empty_and_text_guess_rejected():
    assert parse_guess("", 1, 100)[0] is False
    assert parse_guess("abc", 1, 100)[0] is False
