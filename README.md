# Ember and Tide: AI Quiz Game (Streamlit)

An interactive quiz game for Artificial Intelligence, Units I and II (DSC401-6).
72 questions, 7 formats, 6 chambers, 4 levels, timer, lives, lifelines, score and leaderboard.

## Files

| File | What it does |
| --- | --- |
| `app.py` | The game: screens, scoring, lives, lifelines, timer, scene drawing, leaderboard |
| `questions.py` | The question bank with answers, hints and reasons |
| `requirements.txt` | Python packages (just Streamlit) |
| `.streamlit/config.toml` | Dark theme colours |

## Run on your computer

```
pip install -r requirements.txt
streamlit run app.py
```

## Put it online (Streamlit Community Cloud)

1. Create a free GitHub account and a new public repository, for example `ember-and-tide`.
2. Upload `app.py`, `questions.py`, `requirements.txt`, `README.md` and the `.streamlit` folder.
3. Go to share.streamlit.io, sign in with GitHub, press **Create app**, pick the repository, set the main file to `app.py` and press **Deploy**.
4. After a minute you get a link like `https://your-name-ember-and-tide.streamlit.app`. Submit that link.

## How the game is built

- Session state (`st.session_state`) holds the current screen, the run (deck, lives, score, streak, lifelines) and the current question.
- `build_deck` picks questions for each chamber by level, sorts them easy to hard, and shuffles options.
- `resolve` checks every answer in one place, updates score, streak and lives, and stores the feedback.
- The timer bar is display only. The real time is checked on the server when you submit, so a late answer counts as wrong.
- The leaderboard is saved in `leaderboard.json` on the server and is shared by everyone who plays. On Streamlit Community Cloud it is cleared whenever the app restarts.
