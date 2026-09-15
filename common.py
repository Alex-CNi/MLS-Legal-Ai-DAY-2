import streamlit as st

DIFFICULTY_LABELS = {
    1: "Clueless",
    2: "Casual",
    3: "Decent",
    4: "Sharp",
    5: "Ruthless",
}

# probability the model's move is thrown away for a random legal one
BLUNDER = {1: 0.75, 2: 0.45, 3: 0.20, 4: 0.05, 5: 0.0}

WINS = [(0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)]

DEFAULTS = {
    "difficulty": 3,
    "board": [""] * 9,
    "turn": "X",
    "winner": None,
    "note": "",
}

def init_state():
    """Initialise each key independently so adding a new one never skips it."""
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, list) else value

def check_winner(b):
    for a, c, d in WINS:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    return "Draw" if all(b) else None

def tactical_move(b, mark, opp):
    """Return a winning square, else a blocking square, else None."""
    for target in (mark, opp):
        for a, c, d in WINS:
            line = [b[a], b[c], b[d]]
            if line.count(target) == 2 and line.count("") == 1:
                return (a, c, d)[line.index("")]
    return None