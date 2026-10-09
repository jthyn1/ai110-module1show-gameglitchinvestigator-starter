# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

-  **Purpose:** A Streamlit number-guessing game. Pick a difficulty, then guess a secret number within a limited number of attempts using "Go HIGHER / Go LOWER" hints. Fewer guesses earn a higher score.
-  **Bugs found:** backwards hints; secret turned into a string on even attempts (alphabetical comparisons); "New Game" stuck after a win or loss; Hard range easier than Normal; hard-coded "1 to 100" text; "Attempts left" off by one and lagging a turn; wrong scoring (first-try win = 80, "Too High" could add points); decimals, negatives and out-of-range guesses accepted.
- **Fixes applied:** moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score` (plus a new `get_hint_message`) into `logic_utils.py` and fixed each one. The secret is always compared as an int. A `start_new_game()` helper resets all state and also runs when the difficulty changes. Invalid input shows an error without using an attempt. Each fix is marked with a `# FIX:` comment.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py`. The game opens on **Normal**: "Guess a number between 1 and 50. Attempts left: 8".
2. Pick **Easy** in the sidebar. The range changes to 1–20 with 6 attempts, and a new secret is drawn in that range.
3. Enter a number below the secret and click **Submit Guess**. The hint says "📈 Go HIGHER!", "Attempts left" drops by one, and the score drops by 5.
4. Enter `3.9` (or `-5`, or `abc`). An error message appears and no attempt is used.
5. Enter the correct number. Balloons appear with "You won! … Final score: …" (100 on a first-try win).
6. Click **New Game**. Attempts, score and history reset, and you can play again right away.

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/jerlaptop/Documents/codepath/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collecting ... collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 28%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 35%]
tests/test_game_logic.py::test_single_digit_guess_vs_two_digit_secret PASSED [ 42%]
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED    [ 50%]
tests/test_game_logic.py::test_first_try_win_scores_100 PASSED           [ 57%]
tests/test_game_logic.py::test_too_high_never_adds_points PASSED         [ 64%]
tests/test_game_logic.py::test_negative_guess_rejected PASSED            [ 71%]
tests/test_game_logic.py::test_decimal_guess_rejected PASSED             [ 78%]
tests/test_game_logic.py::test_huge_guess_rejected PASSED                [ 85%]
tests/test_game_logic.py::test_guess_with_spaces_accepted PASSED         [ 92%]
tests/test_game_logic.py::test_empty_and_text_guess_rejected PASSED      [100%]

============================== 14 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
