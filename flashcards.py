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
if "unknown_cards" not in st.session_state:
    st.session_state.unknown_cards = []
if "study_mode" not in st.session_state:
    st.session_state.study_mode = None
if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

# Function to reset study session
def reset_study_session():
    st.session_state.current_card_index = 0
    st.session_state.show_front = True
    st.session_state.unknown_cards = []
    random.shuffle(st.session_state.flashcards)
    st.session_state.review_mode = False

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

    # Display existing flashcards for review and delete
    st.header("Your Flashcards")
    for idx, card in enumerate(st.session_state.flashcards):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"Card {idx + 1}: Front - '{card['front']}', Back - '{card['back']}'")
        with col2:
            if st.button(f"Delete Card {idx + 1}", key=f"delete_{idx}"):
                del st.session_state.flashcards[idx]
                st.experimental_set_query_params()  # Force a rerun to refresh the flashcards list
                return

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

    if st.button("Back to Input Page"):
        st.session_state.page = "input"
        return

    if st.session_state.current_card_index < len(st.session_state.flashcards) or (
        st.session_state.review_mode and st.session_state.current_card_index < len(st.session_state.unknown_cards)
    ):
        # Handle normal or review mode
        if not st.session_state.review_mode:
            card = st.session_state.flashcards[st.session_state.current_card_index]
        else:
            card = st.session_state.unknown_cards[st.session_state.current_card_index]

        # CSS to style the flashcard as a 3x5 card
        card_style = """
        <style>
            .flashcard {
                width: 500px;
                height: 300px;
                border: 2px solid #000;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2);
                margin: 20px auto;
                text-align: center;
                font-size: 24px;
                background-color: #f9f9f9;
            }
        </style>
        """

        st.markdown(card_style, unsafe_allow_html=True)

        # Determine which side to show
        if st.session_state.show_front:
            st.markdown(f"<div class='flashcard'>{card['front']}</div>", unsafe_allow_html=True)
            if st.button("Check Answer"):
                st.session_state.show_front = False
        else:
            st.markdown(f"<div class='flashcard'>{card['back']}</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("I Knew This"):
                    st.session_state.current_card_index += 1
                    st.session_state.show_front = True
            with col2:
                if st.button("I Didn't Know This"):
                    if not st.session_state.review_mode:
                        st.session_state.unknown_cards.append(card)
                    st.session_state.current_card_index += 1
                    st.session_state.show_front = True

    else:
        if not st.session_state.review_mode and st.session_state.unknown_cards:
            st.write("You have completed the initial round of flashcards. Let's review the ones you didn't know.")
            st.session_state.review_mode = True
            st.session_state.current_card_index = 0
            random.shuffle(st.session_state.unknown_cards)
        elif st.session_state.review_mode:
            st.write("You have completed the review session!")
            if st.button("Start Over"):
                reset_study_session()
        else:
            st.write("You have completed all the flashcards!")
            if st.button("Start Over"):
                reset_study_session()

# Navigation between pages
if "page" not in st.session_state:
    st.session_state.page = "input"

if st.session_state.page == "input":
    input_page()
elif st.session_state.page == "study":
    study_page()
