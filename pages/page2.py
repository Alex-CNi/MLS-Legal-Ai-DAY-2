import re
import random
import streamlit as st
from openai import OpenAI
from common import (
    DIFFICULTY_LABELS, BLUNDER,
    init_state, check_winner, tactical_move,
)

client = OpenAI()
init_state()

st.title("Play against GPT-4o")
st.caption(
    f"Difficulty: **{DIFFICULTY_LABELS[st.session_state.difficulty]}** "
    "— change it on the Settings page."
)

def apply_move(i, mark):
    st.session_state.board[i] = mark
    st.session_state.winner = check_winner(st.session_state.board)
    st.session_state.turn = "O" if mark == "X" else "X"

def play(i):
    if st.session_state.board[i] or st.session_state.winner:
        return
    apply_move(i, "X")

def reset():
    st.session_state.board = [""] * 9
    st.session_state.turn = "X"
    st.session_state.winner = None
    st.session_state.note = ""

def ask_model(b, level):
    empty = [i for i, c in enumerate(b) if not c]

    if random.random() < BLUNDER[level]:
        return random.choice(empty), "played a sloppy move"

    grid = "\n".join(
        " | ".join((b[r*3+c] or str(r*3+c)) for c in range(3))
        for r in range(3)
    )
    guidance = (
        "Play to win. Take any winning square. Block any square where X has "
        "two in a row. Otherwise prefer the centre, then a corner."
        if level >= 4 else "Choose a reasonable move."
    )
    prompt = (
        "You are playing tic tac toe as O against a human playing X.\n"
        "Board — digits are empty squares, numbered 0-8 left to right, top to bottom:\n"
        f"{grid}\n\nLegal moves: {empty}\n{guidance}\n"
        "Reply with the square number only."
    )

    try:
        r = client.responses.create(model="gpt-4o", input=prompt)
        m = re.search(r"\d", r.output_text)
        if m and int(m.group()) in empty:
            move = int(m.group())
            if level == 5:
                forced = tactical_move(b, "O", "X")
                if forced is not None and move != forced:
                    return forced, "spotted a forced move"
            return move, None
    except Exception as e:
        return random.choice(empty), f"API error, random move: {e}"

    return random.choice(empty), "illegal reply, random move"

# board
for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        i = row * 3 + col
        cell = st.session_state.board[i]
        cols[col].button(
            {"X": ":blue[**X**]", "O": ":orange[**O**]"}.get(cell, "&nbsp;"),
            key=f"cell_{i}",
            on_click=play,
            args=(i,),
            disabled=bool(cell) or bool(st.session_state.winner)
                     or st.session_state.turn == "O",
            use_container_width=True,
        )

# model's turn
if st.session_state.turn == "O" and not st.session_state.winner:
    level = st.session_state.difficulty
    with st.spinner(f"gpt-4o ({DIFFICULTY_LABELS[level]}) is thinking..."):
        move, note = ask_model(st.session_state.board, level)
    st.session_state.note = note or ""
    apply_move(move, "O")
    st.rerun()

# status
st.write("")
if st.session_state.winner == "Draw":
    st.info("Draw.")
elif st.session_state.winner == "X":
    st.success("You win.")
elif st.session_state.winner == "O":
    st.error("gpt-4o wins.")
else:
    st.write("Your turn.")

if st.session_state.note:
    st.caption(st.session_state.note)

st.button("New game", on_click=reset)