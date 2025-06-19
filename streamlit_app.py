import streamlit as st
import random
import time

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
                "just_correct": False
            }

        fd = st.session_state.fish_data
        q_index = fd["q_index"]

        if fd["caught"] < fish_goal and q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()

            if answer:
                if fd["just_correct"]:
                    time.sleep(1)  # pause to show success message
                    fd["just_correct"] = False
                    st.rerun()
                fd["attempts"] += 1
                if answer == correct:
                    st.success("Well done! You caught a fish! 🐟")
                    fd["caught"] += 1
                    fd["q_index"] += 1
                    fd["attempts"] = 0
                    fd["hint_choice"] = None
                    fd["just_correct"] = True
                    st.rerun()
                else:
                    st.warning("Oops, that's not it.")
                    if fd["attempts"] >= 2:
                        if fd["hint_choice"] is None:
                            want_hint = st.radio(
                                "You're getting tired. Want a mocktail and a hint?",
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
                        st.error("Too many tries! Moving on.")
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
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")

    qa_pairs = [
        ("oink", "pig"),
        ("buzz", "bee"),
        ("moo", "cow"),
        ("meow", "cat"),
        ("cock-a-doodle-doo", "rooster"),
    ]

    # Reset forest_score if new game or first time here
    if "forest_score" not in st.session_state or (choice == "Forest" and st.session_state.get("forest_index", 0) == 0):
        st.session_state.forest_score = 0
        st.session_state.forest_index = 0

    idx = st.session_state.forest_index

    if idx < len(qa_pairs):
        sound, correct_animal = qa_pairs[idx]
        options = [animal for _, animal in qa_pairs]
        random.shuffle(options)

        with st.form(f"form_{idx}"):
            answer = st.radio(f"What animal makes the sound '{sound}'?", options, key=f"forest_radio_{idx}")
            submitted = st.form_submit_button("Submit Answer")
            if submitted:
                if answer == correct_animal:
                    st.session_state.forest_score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Wrong. It's '{correct_animal}'.")
                st.session_state.forest_index += 1
                time.sleep(1)
                st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 You got {score}/{len(qa_pairs)} right!")
        st.balloons()
        st.session_state.progress["Forest"] = True
# ========== RESTART ==========
if all(st.session_state.progress.values()):
    st.markdown("---")
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()

