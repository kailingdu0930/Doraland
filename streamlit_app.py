import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# --- Initialize session state ---
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

# --- Adventure selector ---
st.markdown("### Choose your adventure mode:")
choices = ["Beach", "Desert", "Forest"]
choice = st.selectbox("Where should Dora go?", choices)

# ========== BEACH ==========
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Level 1
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Choose the ingredients that should **NOT** be included in a mocktail:")
        st.info("Hint: There are 3 alcoholic ingredients to pick.")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)

        correct = {"Beer", "Whisky", "Tequila"}
        user = set(selected)

        if len(user) in [1, 2]:
            st.warning("You only selected some answers, there are more!")
        elif user:
            if user == correct:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.rerun()
            else:
                st.error("Oops! Try again — avoid alcoholic ingredients!")

    # Level 2
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        fish_goal = 5
        st.write(f"Dora wants to catch **{fish_goal}** fish! Answer questions correctly to help her.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "Every month has at least 28."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It's outside your body."),
            ("How many days are there in a year?", "365", "Ask someone beside you."),
            ("Which princess ate the poisoned apple?", "snow white", "Classic Disney.")
        ]

        if "fish_data" not in st.session_state:
            st.session_state.fish_data = {
                "caught": 0,
                "q_index": 0,
                "attempts": 0,
                "hint_choice": None,
            }

        fd = st.session_state.fish_data
        q_index = fd["q_index"]

        if fd["caught"] < fish_goal and q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()

            if answer:
                fd["attempts"] += 1
                if answer == correct:
                    st.success("Great! You caught a fish! 🐟")
                    fd["caught"] += 1
                    fd["q_index"] += 1
                    fd["attempts"] = 0
                    fd["hint_choice"] = None
                    st.rerun()
                else:
                    st.warning("Oops, that's not it.")
                    if fd["attempts"] >= 2:
                        if fd["hint_choice"] is None:
                            want_hint = st.radio(
                                "You look tired. Want a mocktail and a hint?",
                                ["No", "Yes"], key=f"hint_{q_index}"
                            )
                            if want_hint == "Yes":
                                fd["hint_choice"] = "Yes"
                                st.session_state.fish_data = fd
                                st.rerun()
                            else:
                                fd["hint_choice"] = "No"
                        if fd["hint_choice"] == "Yes":
                            st.info(f"Hint: {hint}")
                    if fd["attempts"] >= 5:
                        st.error("Too many tries! Moving to the next question.")
                        fd["q_index"] += 1
                        fd["attempts"] = 0
                        fd["hint_choice"] = None
                        st.rerun()

        if fd["caught"] >= fish_goal:
            st.success("🎉 You finished Beach Level 2!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True

# ========== DESERT ==========
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # Level 1
    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.info("Hint: There are 2 incorrect words in the lyrics.")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")

        picks = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])
        if set(picks) == {"butt", "fein"}:
            st.success("Thanks! Boots will now help you on your journey.")
            st.balloons()
            st.session_state.progress["Desert_L1"] = True
            st.session_state.show_desert_l2 = True
            st.rerun()
        elif picks:
            st.error("Try again!")

    # Level 2
    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")

        if "desert2_fail" not in st.session_state:
            st.session_state["desert2_fail"] = 0

        choice2 = st.radio("Choose one:", ["hug", "sing", "dance", "run"], key="desert2")

        if choice2:
            if choice2 == "sing":
                st.success("Boots: That's the spirit! 🎤")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                st.session_state["desert2_fail"] += 1
                st.error("Hmm… not quite.")
                if st.session_state["desert2_fail"] >= 2:
                    st.info("Hint: Think about what helped in the previous level.")

# ========== FOREST ==========
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]

    if "forest_score" not in st.session_state:
        st.session_state.forest_score = 0
        st.session_state.forest_index = 0

    idx = st.session_state.forest_index

    if idx < len(sounds):
        options = animals.copy()
        random.shuffle(options)
        answer = st.selectbox(f"What animal makes the sound '{sounds[idx]}'?", options, key=f"forest_{idx}")
        if st.button("Submit Answer", key=f"submit_{idx}"):
            if answer == animals[idx]:
                st.success("Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It's '{animals[idx]}'.")
            st.session_state.forest_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 You got {score}/{len(sounds)} right!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# ========== RESTART ==========
if all(st.session_state.progress.values()):
    st.markdown("---")
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()

