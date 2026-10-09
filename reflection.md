# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game was very obviously buggy when I first played it. Some examples of what jumped out at me was the game not starting after winning or losing, the prompt asking 1 - 100 despite difficulty, and negative numbers were allowed. It was very clearly in a bad development state that should not have been deployed.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The number of attempts showed one short of what you had.
numbers not in the range, were negative, or decimals all counted as attempts

The game loaded and looked normal, but it was close to impossible to win. Bugs I found:

Hints were backwards. I expected a guess above the secret to say "Go LOWER", but it said "Go HIGHER" (and the other way around). Hints changed from one guess to the next, on every even-numbered attempt the secret was turned into text, so numbers were compared alphabetically. Guessing 9 against 50 said "Too High" because the text "9" sorts after "50". New Game did nothing after a win or loss I expected a fresh game, but the status stayed "won"/"lost", so it kept saying "Game over". It also didn't reset score or history, and it always picked from 1–100 whatever the difficulty. Difficulty and attempts were off. Hard (1–50) had a smaller range than Normal (1–100), the info box always said "between 1 and 100", and "Attempts left" started one short because attempts started at 1. Score was wrong, a first-try win scored 80, not 100, and a "Too High" guess *added* 5 points on even attempts. 3.9 became 3, while -5 and 500 were accepted. Each one used up an attempt.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input                                | Expected Behavior              | Actual Behavior                                                 | Console Output / Error                                                        |
| ------------------------------------ | ------------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Guess 60, secret 50                  | "Too High" / "Go LOWER" hint   | "📈 Go HIGHER!"                                                 | none                                                                          |
| Guess 40, secret 50                  | "Too Low" / "Go HIGHER" hint   | "📉 Go LOWER!"                                                  | none                                                                          |
| Guess 9 on attempt 2, secret 50      | "Too Low"                      | "Too High": secret compared as the string `"50"`                | none                                                                          |
| Win (or lose), then click "New Game" | Fresh game starts              | Still shows "You already won / Game over"; `status` never reset | none                                                                          |
| Select "Hard"                        | Range harder than Normal       | Range 1–50, while Normal is 1–100; info box says "1 and 100"    | none                                                                          |
| Correct guess on first attempt       | Score 100                      | Score 80 (`100 - 10 * (attempt + 1)`)                           | none                                                                          |
| Guess `3.9`                          | Rejected as not a whole number | Accepted as 3, uses an attempt                                  | none                                                                          |
| Run `pytest` on starter code         | Tests run                      | All 3 fail                                                      | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I primarily used Claude Code for this assignment.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI suggested to encode the secret as a number. Before the secret was turned into text on even numbered attempts which caused the hints to fail. By keeping the secret as a number, it makes the comparison a lot easier. I verified this with the pytest case `test_single_digit_guess_vs_two_digit_secret`, which checks that a guess of 9 against a secret of 50 now returns "Too Low" (the old text comparison said "Too High"), and by playing the game, where the hints stayed correct on every attempt instead of flipping on even ones.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

one change that I rejected was the adjustment to the attempts box which wanted to replace the box for an empty placeholder and apply a helper function to operate with st.stop(). I told the AI to simplify this solution so that it would only call one st.info() after the if submit to not have to account for the placeholder block. I verified my version by playing the game: "Attempts left" now drops right after each guess instead of lagging one behind, and once the game is won or lost the box is hidden and only the win/game-over message shows. All 14 pytest tests still passed after the change.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I counted a bug as fixed only when a pytest test reproduced it and now passes, and the live game behaved correctly. I moved the logic into logic_utils.py so it could be tested without Streamlit.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I played the game in the browser: a guess below the secret said "Go HIGHER", 3.9 showed an error without using an attempt, and "New Game" after a win reset attempts, score and status.

- Did AI help you design or understand any tests? How?

Claude Code wrote the tests; I checked that each one targets an actual still-existing bug from my log.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Picture a whiteboard that gets wiped clean and redrawn from top to bottom every time you click a button or type something. The whole page is rebuilt from scratch, so anything written on the board is forgotten unless it's saved somewhere else, which session state is that somewhere else. It's like a notebook beside the whiteboard that doesn't get erased, so the game writes the secret number, your score, and how many guesses you've used in the notebook and copies them back onto the board after each redraw. Anything not in the notebook is forgotten, and anything in it stays until the game changes it, which is why "New Game" got stuck, it never erased the "game over" note, so every redraw still read "game over". The "Attempts left" message was drawn before your guess was counted, so it was always one guess behind until we moved it lower on the page.



---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Something I did while developing the solution was having claude ask for approval for each change it wanted to make, as well as an explanation as to why the change needed to be made. I created this as a skill, which asked the llm to not make any assumptions about what needs to be done, ask for permission at each major step in the development process, return a summary about what is done, and what can alternatively be done. By making this a skill, I can easily recall it in later developments, and it ensures that every decision made is passed through me and there are no assumptions or black-box decisions being made.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time I work with AI, I will try and give it less power over the project. Originally, I let Claude free to work on whatever it saw fit as the best solutions for a given code bug, but this resulted in some of the implementations being less than ideal. As a result, I developed the skill which I mentioned above in order to temper how much it is allowed to do without consulting me first.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project helped me realize how powerful AI generated code can be, but also how that can be dangerous when you don't properly align it with what your vision for a given project is. 