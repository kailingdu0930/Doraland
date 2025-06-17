import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure", page_icon="🧭")
st.title("🗺️ Welcome to Dora Land!")

st.markdown("Characters: Dora, Diego, Boots, Map, Benny the Bull")
choice = st.radio("Where should Dora go first?", ["Beach", "Desert", "Forest"])

# Session state to allow reset
if 'finished' not in st.session_state:
    st.session_state.finished = False

if choice == "Beach" and not st.session_state.finished:
    st.header("🏖️ Beach Adventure")

    # Level 1: Mocktail
    st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
    st.markdown("Diego is struggling to avoid alcoholic ingredients. Help him!")

    ingredients = ["1. Sprite", "2. Lemon", "3. Ginger", "4. Beer", "5. Passion fruit", "6. Whisky", "7. Mint leaf", "8. Tequila"]
    for i in ingredients:
        st.write(i)

    selected = st.text_input("Choose the ingredients that should NOT be included (enter numbers comma-separated, no space)")
    if selected:
        user_set = set(selected.split(","))
        correct = {"4", "6", "8"}
        if user_set == correct:
            st.success("Diego: Thank you! Here's your mocktail! 🍹")
        else:
            st.error("Oops! Try again. Remember, mocktails shouldn't include alcohol.")

    # Level 2: Catching Fish
    st.subheader("🐟 Level 2: Dora wants to catch some fish!")
    if 'fish_level' not in st.session_state:
        st.session_state.fish_level = {
            'target': random.randint(1, 5),
            'caught': 0,
            'index': 0,
            'attempt': 0,
            'fail_count': 0
        }

    fish_q = [
        ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
        ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
        ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
        ("How many days are there in a year?", "365 days", "Ask the person beside you :)"),
        ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
    ]

    if st.session_state.fish_level['caught'] < st.session_state.fish_level['target']:
        q, a, hint = fish_q[st.session_state.fish_level['index']]
        st.markdown(f"**Q:** {q}")
        user_ans = st.text_input("Your answer:", key='fish_q')
        if user_ans:
            if user_ans.strip().lower() == a:
                st.session_state.fish_level['caught'] += 1
                st.success(f"✅ You caught a fish! Total fish: {st.session_state.fish_level['caught']}/{st.session_state.fish_level['target']}")
                st.session_state.fish_level['index'] += 1
                st.session_state.fish_level['attempt'] = 0
            else:
                st.session_state.fish_level['attempt'] += 1
                st.warning("❌ Incorrect.")
                if st.session_state.fish_level['attempt'] == 2 and st.session_state.fish_level['fail_count'] > 2:
                    if st.button("Recharge with mocktail?"):
                        st.info(f"🔋 Hint: {hint}")
                if st.session_state.fish_level['attempt'] >= 5:
                    st.session_state.fish_level['index'] += 1
                    st.session_state.fish_level['attempt'] = 0
                    st.error("😓 Failed this question. Moving on.")
                st.session_state.fish_level['fail_count'] += 1

    if st.session_state.fish_level['caught'] >= st.session_state.fish_level['target']:
        st.balloons()
        st.success("🎉 Congratulation! Dora caught all the fish she wanted!")
        st.session_state.finished = True

elif choice == "Desert" and not st.session_state.finished:
    st.header("🏜️ Desert Journey")

    st.subheader("🎶 Level 1: Fix the Lyrics")
    st.markdown("Boots messed up the lyrics. Help him!")
    st.write("Row, row, row your **butt**")
    st.write("Life is but a **fein**")

    wrong = st.text_input("Type the wrong words (comma-separated)", key="desert1")
    if wrong:
        if set(w.strip().lower() for w in wrong.split(",")) == {"butt", "fein"}:
            st.success("🎉 Correct! Boots will follow you for the rest of the journey!")

            st.subheader("🐂 Level 2: Cheer Up Benny")
            idea = st.text_input("What can we do to help Benny feel better?")
            if idea:
                if idea.strip().lower() in ["sing", "sing a song"]:
                    st.balloons()
                    st.success("🎉 You did it! Benny is smiling now.")
                    st.session_state.finished = True
                else:
                    st.warning("❌ Hmm... try something else.")
                    if st.button("Need a hint?"):
                        st.info("💡 Hint: Use the song from earlier!")
        else:
            st.warning("❌ Not quite. Try again!")

elif choice == "Forest" and not st.session_state.finished:
    st.header("🌲 Forest Animal Sound Game")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "chicken"]
    score = 0

    for i in range(len(sounds)):
        user = st.text_input(f"What animal makes the sound '{sounds[i]}'?", key=f"sound_{i}")
        if user:
            if user.lower() == animals[i]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Oops! It's '{animals[i]}'")

    if st.button("Finish Forest Game"):
        st.balloons()
        st.success(f"🎉 Congratulation! You got {score}/{len(sounds)} correct.")
        st.session_state.finished = True

# Reset button
if st.session_state.finished:
    if st.button("🔄 Restart Adventure"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()




