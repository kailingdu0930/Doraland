import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# 初始化狀態
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

st.markdown("### Choose your adventure mode:")

# 讓玩家自由選擇尚未完成的關卡
available_choices = []
if not st.session_state.progress["Beach_L1"]:
    available_choices.append("Beach")
elif not st.session_state.progress["Beach_L2"]:
    available_choices.append("Beach")

if not st.session_state.progress["Desert_L1"]:
    available_choices.append("Desert")
elif not st.session_state.progress["Desert_L2"]:
    available_choices.append("Desert")

if not st.session_state.progress["Forest"]:
    available_choices.append("Forest")

if not available_choices:
    st.success("🎉 Congratulations! You have completed all adventures!")
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
    st.stop()

choice = st.selectbox("Where should Dora go?", available_choices)

# -------------- Beach Adventure --------------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Level 1
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Diego is struggling to avoid alcoholic ingredients. Help him!")
        st.write("Choose the ingredients that should **NOT** be included in a mocktail:")
        st.info("Hint: There are 3 alcoholic ingredients to pick.")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)

        correct_mocktail = {"Beer", "Whisky", "Tequila"}
        user_set = set(selected)

        if len(user_set) in [1, 2]:
            st.warning("You selected only a few. There are more alcoholic ingredients!")
        elif user_set:
            if user_set == correct_mocktail:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.rerun()
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # Level 2
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catch Fish")
        fish_goal = st.session_state.get("fish_goal", random.randint(1, 5))
        st.session_state.fish_goal = fish_goal
        st.write(f"Dora wants to catch **{fish_goal}** fish! Answer correctly.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean “only” with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        if "fish_data" not in st.session_state:
            st.session_state.fish_data = {
                "caught": 0,
                "q_index": 0,
                "attempts": 0,
                "failed": 0,
                "hint_choice": {}
            }

        fd = st.session_state.fish_data
        q_index = fd.get("q_index", 0)
        caught = fd.get("caught", 0)
        attempts = fd.get("attempts", 0)
        failed = fd.get("failed", 0)
        hint_choice = fd.get("hint_choice", {})

        if caught >= fish_goal:
            st.success("🎉 Congratulations! Hooray, YOU DID IT!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True
            st.rerun()

        elif q_index >= len(questions):
            st.info("Game over. Try again!")
            if st.button("Restart Level 2"):
                st.session_state.fish_data = {
                    "caught": 0,
                    "q_index": 0,
                    "attempts": 0,
                    "failed": 0,
                    "hint_choice": {}
                }
                st.rerun()
        else:
            question, correct_answer, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()

            if answer:
                fd["attempts"] = attempts + 1

                if answer == correct_answer:
                    st.success("Correct! You caught a fish!")
                    st.balloons()
                    fd["caught"] = caught + 1
                    fd["q_index"] = q_index + 1
                    fd["attempts"] = 0
                    fd["failed"] = 0
                    fd["hint_choice"] = {}
                    st.session_state.fish_data = fd
                    st.rerun()
                else:
                    st.error("Incorrect answer.")

                    if fd["attempts"] >= 2 and q_index not in hint_choice:
                        want_hint = st.radio(
                            "It looks like you are exhausted. Would you like to recharge your energy with the mocktail?",
                            ["No", "Yes"],
                            key=f"hint_{q_index}"
                        )
                        fd["hint_choice"][q_index] = want_hint
                        st.session_state.fish_data = fd
                        if want_hint == "Yes":
                            st.info(f"Hint: {hint}")

                    elif q_index in hint_choice and hint_choice[q_index] == "Yes":
                        st.info(f"Hint: {hint}")

                    if fd["attempts"] >= 5:
                        st.warning("You failed this question, moving to the next one.")
                        fd["q_index"] = q_index + 1
                        fd["attempts"] = 0
                        fd["failed"] = failed + 1
                        fd["hint_choice"] = {}
                        st.session_state.fish_data = fd
                        st.rerun()

                st.session_state.fish_data = fd


# -------------- Desert Adventure --------------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.info("Hint: There are 2 incorrect words in the lyrics.")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")

        desert_input = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])
        if set(desert_input) == {"butt", "fein"}:
            st.success("Thank you Dora! Now Boots will help you on your journey!")
            st.balloons()
            st.session_state.progress["Desert_L1"] = True
            st.session_state.show_desert_l2 = True
            st.rerun()
        elif desert_input:
            st.error("Not quite right. Try again!")

    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")
        options = ["hug", "sing", "dance", "run"]
        choice_desert2 = st.radio("Choose one way to help:", options, key="desert2")
        if choice_desert2:
            if choice_desert2 == "sing":
                st.success("Boots: What a good suggestion! Let's sing! 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                fail_count = st.session_state.get("desert2_fail", 0) + 1
                st.session_state["desert2_fail"] = fail_count
                if fail_count >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.error("Hmm… Try something else!")

# -------------- Forest Adventure --------------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]

    if "forest_score" not in st.session_state:
        st.session_state.forest_score = 0
        st.session_state.forest_index = 0

    idx = st.session_state.forest_index
    if idx < len(sounds):
        # Shuffle options for difficulty
        options = ["pig", "bee", "cow", "cat", "rooster"]
        random.seed(idx)  # Make shuffle deterministic per question
        random.shuffle(options)
        answer = st.selectbox(f"What animal makes this sound '{sounds[idx]}'?", options, key=f"forest_{idx}")
        if st.button("Submit Answer", key=f"submit_{idx}"):
            if answer == animals[idx]:
                st.success("Correct! Moving to the next sound.")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was '{animals[idx]}'.")
            st.session_state.forest_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulations! You got {score}/{len(sounds)} correct!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# Restart button
if st.session_state.progress["Beach_L2"] and st.session_state.progress["Desert_L2"] and st.session_state.progress["Forest"]:
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()

