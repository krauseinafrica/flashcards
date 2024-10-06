import streamlit as st
import pandas as pd
import random

# Store flashcards in session state
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_card_index" not in st.session_state:
    st.session_state.current_card_index = 0
if "show_front" not in st.session_state:
    st.session_state.show_front = True

# Function to reset study session
def reset_study_session():
    st.session_state.current_card_index = 0
    st.session_state.show_front = True
    random.shuffle(st.session_state.flashcards)

# Page 1: Flashcard Input
def input_page():
    st.title("Flashcard Study Tool")

    # Choose Input Method
    st.header("Choose Input Method")
    input_method = st.radio("How would you like to provide flashcards?", ["Upload CSV", "Add Manually"])

    # Upload CSV
    if input_method == "Upload CSV":
        uploaded_file = st.file_uploader("Upload a CSV file with 'Front' and 'Back' columns", type="csv")
        if uploaded_file is not None:
            try:
                # Read CSV and add to flashcards list
                df = pd.read_csv(uploaded_file)
                if "Front" in df.columns and "Back" in df.columns:
                    for _, row in df.iterrows():
                        st.session_state.flashcards.append({"front": row["Front"], "back": row["Back"]})
                    st.success("Flashcards from CSV file added!")
                else:
                    st.error("CSV file must contain 'Front' and 'Back' columns.")
            except Exception as e:
                st.error(f"An error occurred while reading the CSV file: {e}")

    # Add Manually
    elif input_method == "Add Manually":
        st.header("Create Flashcards Manually")
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

    # Study Options and Start Studying
    if st.session_state.flashcards:
        study_mode = st.selectbox("Select study mode:", ["Show Front Only", "Show Back Only", "Random Front/Back"])
        if st.button("Start Studying"):
            st.session_state.study_mode = study_mode
            reset_study_session()
            st.session_state.page = "study"

# Page 2: Study Session
def study_page():
    st.title("Flashcard Study Session")

    if st.session_state.current_card_index < len(st.session_state.flashcards):
        card = st.session_state.flashcards[st.session_state.current_card_index]

        # Determine which side to show
        if st.session_state.study_mode == "Show Front Only":
            st.write(f"Front: {card['front']}")
            if st.button("Next"):
                st.session_state.current_card_index += 1

        elif st.session_state.study_mode == "Show Back Only":
            st.write(f"Back: {card['back']}")
