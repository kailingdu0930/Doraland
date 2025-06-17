import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# Initialize progress state
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

# Helper function for congratulations message and balloons
def finish_path(path_key):
    st.success("🎉 Congratulations! You completed this part!")
    st.balloons()
    st.session_state.progress[path_key] = True

# Select adventure path
available_paths = []
if not st.session_state.progress["Beach_L1"] or (st.session_state.progress["Beach_L1"] and not st.session_state.progress["Beach_L2"]):
    available_paths.append("Beach")
if not st.session_state.progress["Desert_L1"] or (st.session_state.progress["Desert_L1"] and not st.session_state.progress["Desert_L2"]):
    available_paths.append("Desert")
if not st.session_state.progress["Forest"]:
    available_paths.append("Forest")

choice = st.selectbox("Choose your adventure:", available_paths)

# ---------------- Beach Adventure ----------------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Beach Level 1
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Choose the ingredients that should **NOT** be included in a mocktail:")
        st.info("Hint: There are 3 alcoholic ingredients.")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)

        correct_mocktail = {"Beer", "Whisky", "Tequila"}
        user_set = set(selected)

        if len(user_set) in [1, 2]:
            st.warning("You selected only some answers, there are more.")
        elif user_set:
            if user_set == correct_mocktail:
                st.success("Well done! Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.button("Go to Level 2", on_click=lambda: st.rerun())
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # Beach Level 2
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        # Initialize level 2 variables
        if "fish_goal" not in st.session_state:
            st.session_state.fish_goal = random.randint(1, 5)
        if "fish_q_index" not in st.session_state:
            st.session_state.fish_q_index = 0
        if "fish_caught" not in st.session_state:
            st.session_state.fish_caught = 0
        if "fish_attempts" not in st.session_state:
            st.session_state.fish_attempts = 0

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        caught = st.session_state.fish_caught
        q_idx = st.session_state.fish_q_index

        st.write(f"Dora wants to catch **{st.session_state.fish_goal}** fish!")

        if caught < st.session_state.fish_goal and q_idx < len(questions):
            question, answer, hint = questions[q_idx]
            st.write(f"Q{q_idx + 1}: {question}")

            user_answer = st.text_input("Your answer:", key=f"fish_{q_idx}").strip().lower()

            if user_answer:
                if user_answer == answer:
                    st.success("Well done! You caught a fish! 🎉")
                    st.session_state.fish_caught += 1
                    st.session_state.fish_q_index += 1
                    st.session_state.fish_attempts = 0
                    st.rerun()
                else:
                    st.session_state.fish_attempts += 1
                    st.warning("Oops, that's not right. Try again!")
                    if st.session_state.fish_attempts == 2:
                        want_hint = st.radio("You look tired. Recharge with a mocktail for a hint?", ["No", "Yes"], key=f"hint_choice_{q_idx}")
                        if want_hint == "Yes":
                            st.info(f"Hint: {hint}")
                    if st.session_state.fish_attempts >= 5:
                        st.error("You've failed this question, moving on.")
                        st.session_state.fish_q_index += 1
                        st.session_state.fish_attempts = 0
                        st.rerun()
        else:
            finish_path("Beach_L2")

# ---------------- Desert Adventure ----------------
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
        if desert_input:
            if set(desert_input) == {"butt", "fein"}:
                st.success("Well done! Thank you Dora! Now Boots will help you on your journey!")
                st.session_state.progress["Desert_L1"] = True
                st.session_state.show_desert_l2 = True
                st.button("Go to Level 2", on_click=lambda: st.rerun())
            else:
                st.error("Not quite right. Try again!")

    # Desert Level 2
    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")
        options = ["hug", "sing", "dance", "run"]
        choice2 = st.radio("Choose one way to help:", options, key="desert2_choice")
        if choice2:
            if choice2 == "sing":
                st.success("Well done! Boots: What a good suggestion! Let's sing! 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                st.session_state["desert2_fail"] = st.session_state.get("desert2_fail", 0) + 1
                if st.session_state["desert2_fail"] >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.error("Hmm… Try something else!")

# ---------------- Forest Adventure ----------------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]

    if "forest_score" not in st.session_state:
        st.session_state.forest_score = 0
    if "forest_index" not in st.session_state:
        st.session_state.forest_index = 0

    idx = st.session_state.forest_index

    if idx < len(sounds):
        import random
        choices = animals.copy()
        random.shuffle(choices)

        selected = st.selectbox(f"What animal makes this sound '{sounds[idx]}'?", choices, key=f"forest_{idx}")
        if st.button("Submit Answer", key=f"forest_submit_{idx}"):
            if selected == animals[idx]:
                st.success("Well done! Correct!")
                st.session_state.forest_score += 1
                st.session_state.forest_index += 1
                st.rerun()
            else:
                st.error(f"Wrong. The correct answer was '{animals[idx]}'. Moving on.")
                st.session_state.forest_index += 1
                st.rerun()
    else:
        finish_path("Forest")

# Restart button when all paths done
if all(st.session_state.progress.values()):
    if st.button("🔄 Restart Adventure"):
        for key in st.session_state.progress:
            st.session_state.progress[key] = False
        st.session_state.show_beach_l2 = False
        st.session_state.show_desert_l2 = False
        for key in ["fish_goal", "fish_q_index", "fish_caught", "fish_attempts", "forest_score", "forest_index", "desert2_fail"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


