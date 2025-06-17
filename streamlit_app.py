import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# Initialize session state
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
choices = ["Beach", "Desert", "Forest"]
choice = st.selectbox("Where should Dora go?", choices)

# -------------- Beach Adventure --------------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Beach Level 1
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
            st.warning("You only selected some answers, there are more!")
        elif user_set:
            if user_set == correct_mocktail:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.rerun()
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # Beach Level 2
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        # Fixed fish goal to 5 every time as requested
        fish_goal = 5
        st.session_state.fish_goal = fish_goal
        st.write(f"Dora wants to catch **{fish_goal}** fish! Answer questions correctly to help her.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
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
                "hint_shown": False,
                "hint_choice": None,
            }

        fish_data = st.session_state.fish_data
        q_index = fish_data["q_index"]
        caught = fish_data["caught"]
        attempts = fish_data["attempts"]

        if caught < fish_goal and q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()

            if answer:
                fish_data["attempts"] += 1
                if answer == correct:
                    st.success("Well done! You caught a fish!")
                    fish_data["caught"] += 1
                    fish_data["q_index"] += 1
                    fish_data["attempts"] = 0
                    fish_data["hint_shown"] = False
                    fish_data["hint_choice"] = None
                    st.rerun()
                else:
                    st.warning("Incorrect.")
                    # After 2 failed attempts show hint option if not already chosen
                    if fish_data["attempts"] == 2 and fish_data["hint_choice"] is None:
                        want_hint = st.radio(
                            "It looks like you are exhausted. Would you like to recharge your energy with the mocktail?", 
                            ["No", "Yes"], key=f"hint_choice_{q_index}")
                        fish_data["hint_choice"] = want_hint
                        if want_hint == "Yes":
                            st.info(f"Hint: {hint}")
                    elif fish_data["hint_choice"] == "Yes":
                        st.info(f"Hint: {hint}")
                    # If 5 attempts exceeded, fail question and move on
                    if fish_data["attempts"] >= 5:
                        st.error("You failed this question.")
                        fish_data["q_index"] += 1
                        fish_data["attempts"] = 0
                        fish_data["hint_shown"] = False
                        fish_data["hint_choice"] = None
                        st.rerun()

        if caught >= fish_goal:
            st.success("🎉 Congratulations! You completed Beach Level 2!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True

# -------------- Desert Adventure --------------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # Desert Level 1
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

    # Desert Level 2
    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")
        options = ["hug", "sing", "dance", "run"]
        choice2 = st.radio("Choose one way to help:", options, key="desert2")

        if choice2:
            if choice2 == "sing":
                st.success("Boots: What a good suggestion! Let's sing! 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                if st.session_state.get("desert2_fail", 0) >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.session_state["desert2_fail"] = st.session_state.get("desert2_fail", 0) + 1
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
        # Shuffle options each question
        options = animals.copy()
        random.shuffle(options)

        answer = st.selectbox(f"What animal makes this sound '{sounds[idx]}'?", options, key=f"forest_{idx}")
        if st.button("Submit Answer", key=f"submit_{idx}"):
            if answer == animals[idx]:
                st.success("Well done! Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. The correct answer is '{animals[idx]}'")
            st.session_state.forest_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulations! You got {score}/{len(sounds)} correct!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# Restart button (only appears when all paths are done)
if all(st.session_state.progress.values()):
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()

