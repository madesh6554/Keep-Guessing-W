# Word Chain Infinity

A word chain party game for the browser. Each word must start with the last letter of the word before it. No repeats, beat the clock, last player standing wins.

**Play:** https://madesh6554.github.io/Keep-Guessing-W/

## Features

- **Modes:** Classic, Survival (clock speeds up), Category (Animals, Food, Nature, Home, Jobs, Sports), Word Race (word limit, top score wins), 60-second Blitz
- **Infinity Stages:** endless levels against a rival bot, with 1–3 stars per stage and progress saved in your browser
- **Players:** up to 8, any mix of friends (pass-and-play on one device) and bots (Easy / Medium / Hard)
- **Rules you can change before and during a game:** turn timer, shortest word, lives, every-5th-word-grows challenge, speed up, real words only, no proper names, category, word limit
- **Dictionary of ~64,000 English words**, plus a proper-name list for the "No proper names" rule
- Animated characters, sound effects, hints, streak scoring, confetti

## Files

| File | What it is |
|---|---|
| `index.html` | The whole game: layout, styles and game logic (HTML + CSS + JavaScript) |
| `words.js` | Generated dictionary, bot vocabulary and category lists |
| `build_words.py` | Python script that builds `words.js` |

## Run it locally

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy on GitHub Pages

1. Push `index.html`, `words.js`, `build_words.py` and `README.md` to the `main` branch.
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch **main**, folder **/ (root)**, then **Save**.
4. After a minute or two the game is live at `https://<your-username>.github.io/<repo-name>/`.

## Rebuild the word list (optional)

```bash
sudo apt install wamerican      # English word list
pip install wordfreq            # word frequencies for the bots
python3 build_words.py          # writes words.js
```

Edit the `CATEGORIES` dictionary in `build_words.py` to add your own themes.

## Ideas for later

Online multiplayer needs a small server (for example Python with FastAPI + WebSockets) because GitHub Pages only hosts static files.
