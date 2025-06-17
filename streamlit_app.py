import streamlit as st
import random

st.set_page_config(page_title="Dora Land", page_icon="🗽️")
st.title("🗽️ Welcome to Dora Land!")

st.subheader("Where should Dora go first?")
choice = st.radio("Choose a path:", ["Beach", "Desert (Coming Soon)", "Forest (Coming Soon)"])

if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    if "beach_level" not in st.session_state:
        st.session_state.beach_level = 1

    # Level 1: Mocktail
    if st.session_state.beach_level == 1:
        st.subheader("Level 1: Help Diego Make a Mocktail")
        st.write("Diego: Ohh, what a good day! Nice to meet you Dora! I'm making mocktails but struggling to avoid alcoholic ingredients. Can you help me?")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        st.write("Ingredients:")
        st.write(", ".join(ingredients))

        wrong_choices = st.multiselect("Choose ingredients that should NOT be in a mocktail:", ingredients)

        if st.button("Submit Mocktail Choices"):
            if set(wrong_choices) == {"Beer", "Whisky", "Tequila"}:
                st.success("Diego: Thank you! Here's your mocktail! 🍹")
                st.session_state.beach_level = 2
            else:
                st.error("Oops! Try again. Mocktails shouldn't include alcohol.")

    # Level 2: Catching Fish Trial 1
    elif st.session_state.beach_level == 2:
        st.subheader("Level 2: Trial 1 - Dora wants to catch some fish!")

        if "q_index" not in st.session_state:
            st.session_state.q_index = 0
            st.session_state.trial_one_correct = 0

        questions = [
            ("Which month has twenty-eight days?", "every month"),
            ("Who drew the artwork, The Starry Night?", "van gogh"),
            ("What is the biggest organ of the human body?", "skin"),
            ("How many days are there in a year?", "365 days"),
            ("Which of the princesses ate the poisoned apple?", "snow white")
        ]

        if st.session_state.q_index < len(questions):
            q, correct = questions[st.session_state.q_index]
            with st.form(key=f"fish_trial1_form_{st.session_state.q_index}"):
                user_answer = st.text_input(f"Question {st.session_state.q_index+1}: {q}")
                submit = st.form_submit_button("Submit Answer")

            if submit:
                if user_answer.strip().lower() == correct:
                    st.success("✅ Correct!")
                    st.session_state.trial_one_correct += 1
                else:
                    st.error("❌ Incorrect!")
                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success(f"You answered {st.session_state.trial_one_correct} out of {len(questions)} correctly!")
            if st.button("Next Trial"):
                st.session_state.beach_level = 3
                del st.session_state.q_index
                del st.session_state.trial_one_correct
                st.rerun()

    # Level 3: Placeholder for more trials
    elif st.session_state.beach_level == 3:
        st.success("🎉 Welcome to Trial 2! (Coming soon)")
        if st.button("Restart Beach Levels"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

elif choice == "Desert (Coming Soon)":
    st.write("🐵 Boots is singing. Can you spot the wrong lyrics?")
    lyrics = "Row, row, row your **butt**, gently down the stream,\nMerrily, merrily, merrily, merrily, life is but a **fein**."
    st.code(lyrics)
    wrong_words = st.multiselect("Which words are incorrect?", ["boat", "butt", "dream", "fein"])
    if st.button("Submit"):
        if set(wrong_words) == {"butt", "fein"}:
            st.success("Correct! Those lyrics are wrong.")
        else:
            st.error("Hmm, not quite right!")

elif choice == "Forest (Coming Soon)":
    st.write("🌳 Map wants help matching animal sounds.")
    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]
    score = 0

    for sound, correct_animal in zip(sounds, animals):
        guess = st.text_input(f"What animal makes this sound: '{sound}'?", key=sound)
        if guess.lower().strip() == correct_animal:
            score += 1

    if st.button("Check Score"):
        st.write(f"You got {score} out of {len(sounds)} correct.")




