import streamlit as st

st.title("🗺️ Welcome to Dora Land!")

st.subheader("Where should Dora go first?")
choice = st.radio("Choose a path:", ["Beach", "Desert", "Forest"])

if choice == "Beach":
    st.write("🏖️ Diego is making a mocktail! Help him find ingredients that shouldn't be in it.")
    st.write("Ingredients: Sprite, Lemon, Ginger, Beer, Passion fruit, Whisky, Mint leaf, Tequila")
    wrong = st.multiselect("Which ingredients should NOT be included in a mocktail?", 
                           ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"])
    if set(wrong) == {"Beer", "Whisky", "Tequila"}:
        st.success("Correct! No alcohol in mocktails!")
    else:
        st.error("Oops! Try again. 🍹")

elif choice == "Desert":
    st.write("🐵 Boots is singing. Can you spot the wrong lyrics?")
    lyrics = "Row, row, row your **butt**, gently down the stream,\nMerrily, merrily, merrily, merrily, life is but a **fein**."
    st.code(lyrics)
    wrong_words = st.multiselect("Which words are incorrect?", ["boat", "butt", "dream", "fein"])
    if set(wrong_words) == {"butt", "fein"}:
        st.success("Correct! Those lyrics are wrong.")
    else:
        st.error("Hmm, not quite right!")

else:
    st.write("🌳 Map wants help matching animal sounds.")
    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "chicken"]
    score = 0
    for sound, correct_animal in zip(sounds, animals):
        guess = st.text_input(f"What animal makes this sound: '{sound}'?", key=sound)
        if guess.lower().strip() == correct_animal:
            score += 1
    if st.button("Check Score"):
        st.write(f"You got {score} out of {len(sounds)} correct.")
