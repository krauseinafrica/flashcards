import streamlit as st
import random

# Store flashcards in session state
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

# Flashcard Input UI
st.title("Flashcard Study Tool")

st.header("Create Flashcards")
front = st.text_input("Front of Card")
back = st.text_input("Back of Card")
if st.button("Add Card"):
    if front and back:
        st.session_state.flashcards.append({"front": front, "back": back})
        st.success("Flashcard added!")
    else:
        st.error("Both front and back fields must be filled.")

# Display existing flashcards for review
st.header("Your Flashcards")
for idx, card in enumerate(st.session_state.flashcards):
    st.write(f"Card {idx + 1}: Front - '{card['front']}', Back - '{card['back']}'")

# Study Options
st.header("Study Options")
study_mode = st.selectbox("Select study mode:", ["Show Front Only", "Show Back Only", "Random Front/Back"])

# Start Studying
if st.button("Start Studying"):
    if not st.session_state.flashcards:
        st.error("No flashcards available. Please add some flashcards first.")
    else:
        # Randomize flashcards
        flashcards = st.session_state.flashcards.copy()
        random.shuffle(flashcards)

        st.header("Flashcards")
        for card in flashcards:
            if study_mode == "Show Front Only":
                st.write(f"Front: {card['front']}")
            elif study_mode == "Show Back Only":
                st.write(f"Back: {card['back']}")
            elif study_mode == "Random Front/Back":
                side = random.choice(["front", "back"])
                st.write(f"{'Front' if side == 'front' else 'Back'}: {card[side]}")

