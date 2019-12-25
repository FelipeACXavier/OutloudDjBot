# Outloud Bot

Basic bot to automatic handle votes in the [outloud dj](https://outloud.dj/) app.

## Usage
---
To run the tool use:

    python bot.py "options"

For all the options use the help flag:

    python bot.py --help

Available options are

- To upvote or just add a song
- Which song
- Which artist
- How many votes to cast per song
- Use song file (see example: songs.csv)

### Notes

This bot uses [selenium](https://selenium-python.readthedocs.io/) and geckodriver with
the [chrome webdriver](https://chromedriver.chromium.org/). Make sure those are installed
before using it.

## Todo
---
- Implement multi-threading, now there are only two votes been cast and  it is still quite slow.
- Add option to downvote a song
- Clean up code
- Maybe add control through app?
