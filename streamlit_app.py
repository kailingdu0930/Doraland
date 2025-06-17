import streamlit as st
import random

st.set_page_config(page_title="Dora Land", page_icon="🗺️")
st.title("🗺️ Welcome to Dora Land!")

st.subheader("Where should Dora go first?")
choice = st.radio("Choose a path:", ["Beach", "Desert (Coming Soon)", "Forest (Coming Soon)"])

if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Level 1: Mocktail
    st.subheader("Level 1: Help Diego Make a Mocktail")
    st.write("Diego: Ohh, what a good day! Nice to meet you Dora! I'm making mocktails but struggling to avoid alcoholic ingredients. Can you help me?")
    ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
    st.write("Ingredients:")
    st.write(", ".join(ingredients))

    wrong_choices = st.multiselect("Choose ingredients that should NOT be in a mocktail:", ingredients)

    if st.button("Submit Mocktail Choices"):
        if set(wrong_choices) == {"Beer", "Whisky", "Tequila"}:
            st.success("Diego: Thank you for helping me finish the drink Dora! Here's your delicious mocktail! 🍹")
        else:
            st.error("Oops! Try again. Mocktails shouldn't include alcohol.")

    st.markdown("---")

    # Level 2: Catching Fish
    st.subheader("Level 2: Dora wants to catch some fish!")

    # 初始化狀態
    if "target_fish" not in st.session_state:
        st.session_state.target_fish = random.randint(1, 5)
        st.session_state.caught_fish = 0
        st.session_state.q_index = 0
        st.session_state.feedback = ""

    st.write(f"Dora wants to catch {st.session_state.target_fish} fish by answering questions!")

    questions = [
        ("Which month has twenty-eight days?", "every month", "All months have at least 28 days."),
        ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
        ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body."),
        ("How many days are there in a year?", "365 days", "Ask the person beside you :)"),
        ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
    ]

    if st.session_state.caught_fish >= st.session_state.target_fish:
        st.success("🎉 Hooray, YOU DID IT! Dora caught all the fish she wanted!")
    elif st.session_state.q_index >= len(questions):
        st.error("😢 Oh no! Dora didn't catch enough fish. Better luck next time!")
    else:
        q, correct, hint = questions[st.session_state.q_index]

        with st.form(key="answer_form"):
            user_answer = st.text_input(f"Question {st.session_state.q_index+1}: {q}")
            submit = st.form_submit_button("Submit Answer")

        if submit:
            if user_answer.strip().lower() == correct:
                st.session_state.caught_fish += 1
                st.session_state.feedback = "✅ Correct! You caught a fish!"
            else:
                st.session_state.feedback = f"❌ Incorrect! Hint: {hint}"
            st.session_state.q_index += 1

        if st.session_state.feedback:
            if "Correct" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.warning(st.session_state.feedback)

elif choice == "Desert":
    st.write("🐵 Boots is singing. Can you spot the wrong lyrics?")
    lyrics = "Row, row, row your **butt**, gently down the stream,\nMerrily, merrily, merrily, merrily, life is but a **fein**."
    st.code(lyrics)
    wrong_words = st.multiselect("Which words are incorrect?", ["boat", "butt", "dream", "fein"])
    if st.button("Submit"):
        if set(wrong_words) == {"butt", "fein"}:
            st.success("Correct! Those lyrics are wrong.")
        else:
            st.error("Hmm, not quite right!")

else:
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




