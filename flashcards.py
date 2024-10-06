import streamlit as st
import pandas as pd
import random

# Store flashcards in session state
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

# Flashcard Input UI
st.title("Flashcard Study Tool")

# Option to Upload CSV File
st.header("Upload Flashcards from CSV")
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

# Option to Manually Add Flashcards
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

# Study Options
st.header("Study Options")
study_mode = st.selectbox("Select study mode:", ["Show Front Only", "Show Back Only", "Random Front/Back"])

# Start Studying
if st.button("Start Studying"):
    if not st.session_state.flashcards:
        s
