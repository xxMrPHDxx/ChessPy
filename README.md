# ChessPy

### About
A ported version of Chess-Cpp (C++ & SFML) and Chess (Java) into python using Python 3.

### How to play
- Click on piece to select
- Click on highlighted tile (if any for the second time) to execute the specific move
- `CTRL` + `Z` to undo your move

### How to run (Without test)
1) Make sure you have Python 3.8+ installed. Go to python 3 download [page](https://www.python.org/downloads/)
2) Run in terminal/cmd `python board.py` or `python3 board.py`

### How to run test cases
1) Install **flake8** and **pytest** using pip. `pip install flake8 pytest`
2) Run lint using `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
3) Run tests using `pytest` or `pytest test_sample.py` for specific test