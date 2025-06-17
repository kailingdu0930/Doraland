import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# ----------- Session State Setup -----------
if "progress" not in st.session_state:
    st.session_state.progress = {
        "Beach_L1": False,
        "Beach_L2": False,
        "Desert_L1": False,
        "Desert_L2": False,
        "Forest": False
    }

if "show_beach_l2" not in st.session_state:
    st.session_state.show_beach_l2 = False
if "show_desert_l2" not in st.session_state:
    st.session_state.show_desert_l2 = False

# ----------- Adventure Select Menu -----------
if st.session_state.progress["Beach_L2"] and st.session_state.progress["Desert_L2"] and st.session_state.progress["Forest"]:
    st.success("🎉 Hooray, YOU DID IT!")
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.experimental_rerun()
    st.stop()

st.markdown("### Choose your adventure mode:")
available_choices = ["", "Beach"]
if st.session_state.progress["Beach_L2"]:
    available_choices.append("Desert")
if st.session_state.progress["Desert_L2"]:
    available_choices.append("Forest")

choice = st.selectbox("Where should Dora go?", available_choices)

# ----------- Beach Adventure -----------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # ---- Beach Level 1 ----
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Choose the ingredients that should **NOT** be included in a mocktail:")
        st.info("Hint: There are 3 alcoholic ingredients to pick.")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)
        correct_set = {"Beer", "Whisky", "Tequila"}

        if selected:
            user_set = set(selected)
            if user_set == correct_set:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.experimental_rerun()
            elif len(selected) < 3:
                st.warning("Almost there! There are more alcoholic ingredients to find!")
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # ---- Beach Level 2 ----
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        if "fish_data" not in st.session_state:
            fish_goal = random.randint(1, 5)
            st.session_state.fish_data = {
                "goal": fish_goal,
                "caught": 0,
                "q_index": 0,
                "attempts": 0,
                "failed": 0,
                "hint_ready": False
            }

        q_data = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean \"only\" with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        data = st.session_state.fish_data
        if data["caught"] < data["goal"] and data["q_index"] < len(q_data):
            question, answer, hint = q_data[data["q_index"]]
            st.write(f"Dora wants **{data['goal']}** fish. You've caught: {data['caught']}")
            st.write(f"Q: {question}")
            user_answer = st.text_input("Your answer:", key=f"fish_{data['q_index']}").strip().lower()

            if user_answer:
                data["attempts"] += 1
                if user_answer == answer:
                    data["caught"] += 1
                    data["q_index"] += 1
                    data["attempts"] = 0
                    data["hint_ready"] = False
                    st.success("🎣 You caught a fish!")
                    st.experimental_rerun()
                else:
                    st.warning("❌ Incorrect.")
                    if data["attempts"] == 2:
                        data["hint_ready"] = True
                    if data["attempts"] >= 5:
                        st.error("😓 You failed this question.")
                        data["q_index"] += 1
                        data["attempts"] = 0
                        data["failed"] += 1
                        data["hint_ready"] = False
                        st.experimental_rerun()

            if data["hint_ready"]:
                use_hint = st.radio("It looks like you're exhausted. Want to recharge with the mocktail?", ["Yes", "No"], key=f"hint_{data['q_index']}")
                if use_hint == "Yes":
                    st.info(f"Hint: {hint}")

        elif data["caught"] >= data["goal"]:
            st.success("🎉 Hooray, YOU DID IT!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True
            st.experimental_rerun()

# ----------- Desert Adventure -----------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # ---- Desert Level 1 ----
    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Row, row, row your butt\nGently down the stream\nMerrily, merrily, merrily, merrily\nLife is but a fein")
        desert_input = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])
        if set(desert_input) == {"butt", "fein"}:
            st.success("Boots: Thank you Dora! I'll sing it right next time!")
            st.balloons()
            st.session_state.progress["Desert_L1"] = True
            st.session_state.show_desert_l2 = True
            st.experimental_rerun()
        elif desert_input:
            st.error("Hmm... try again!")

    # ---- Desert Level 2 ----
    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        desert2_input = st.text_input("What can we do to help Benny feel better?", key="desert2").strip().lower()
        if desert2_input:
            if desert2_input in {"sing", "sing a song"}:
                st.success("Boots: What a great idea! Let's sing together 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.experimental_rerun()
            else:
                st.error("Hmm… Try something else!")

# ----------- Forest Adventure -----------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]
    options = ["pig", "bee", "cow", "cat", "rooster", "dog", "sheep", "duck"]

    if "forest_index" not in st.session_state:
        st.session_state.forest_index = 0
        st.session_state.forest_score = 0

    idx = st.session_state.forest_index
    if idx < len(sounds):
        choice = st.radio(f"What animal makes this sound: '{sounds[idx]}'", options, key=f"forest_q_{idx}")
        if st.button("Submit", key=f"submit_forest_{idx}"):
            if choice == animals[idx]:
                st.success("Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was '{animals[idx]}'")
            st.session_state.forest_index += 1
            st.experimental_rerun()
    else:
        st.success(f"🎉 You got {st.session_state.forest_score}/{len(sounds)} correct!")
        st.balloons()
        st.session_state.progress["Forest"] = True
        st.experimental_rerun()

# ----------- Restart Button -----------
if st.button("🔄 Restart Adventure"):
    st.session_state.clear()
    st.experimental_rerun()

