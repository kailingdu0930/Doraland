import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# Initialize progress and other session state variables
if "progress" not in st.session_state:
    st.session_state.progress = {
        "Beach_L1": False,
        "Beach_L2": False,
        "Desert_L1": False,
        "Desert_L2": False,
        "Forest": False,
    }

if "show_beach_l2" not in st.session_state:
    st.session_state.show_beach_l2 = False
if "show_desert_l2" not in st.session_state:
    st.session_state.show_desert_l2 = False

# Fish level session state initialization
if "fish_goal" not in st.session_state:
    st.session_state.fish_goal = random.randint(1, 5)
if "fish_q_index" not in st.session_state:
    st.session_state.fish_q_index = 0
if "fish_caught" not in st.session_state:
    st.session_state.fish_caught = 0
if "fish_attempts" not in st.session_state:
    st.session_state.fish_attempts = 0
if "fish_failed" not in st.session_state:
    st.session_state.fish_failed = 0
if "want_hint" not in st.session_state:
    st.session_state.want_hint = False

# Forest level session state initialization
if "forest_q_index" not in st.session_state:
    st.session_state.forest_q_index = 0
if "forest_score" not in st.session_state:
    st.session_state.forest_score = 0

# Desert level 2 fail count
if "desert2_fail" not in st.session_state:
    st.session_state.desert2_fail = 0

st.markdown("### Choose your adventure mode:")

available_choices = []
# You can always select any not yet fully completed area
if not st.session_state.progress["Beach_L1"] or not st.session_state.progress["Beach_L2"]:
    available_choices.append("Beach")
if not st.session_state.progress["Desert_L1"] or not st.session_state.progress["Desert_L2"]:
    available_choices.append("Desert")
if not st.session_state.progress["Forest"]:
    available_choices.append("Forest")

choice = st.selectbox("Where should Dora go?", options=available_choices)

# ------------------- Beach Adventure -------------------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Level 1: Mocktail ingredients
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
            st.warning("You have selected only a few answers, there are more!")
        elif user_set:
            if user_set == correct_mocktail:
                st.success("Well done! Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.rerun()
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # Level 2: Catch fish quiz
    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        st.write(f"Dora wants to catch **{st.session_state.fish_goal}** fish! Answer questions correctly to help her.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        q_idx = st.session_state.fish_q_index
        caught = st.session_state.fish_caught
        attempts = st.session_state.fish_attempts
        failed = st.session_state.fish_failed

        if caught < st.session_state.fish_goal and q_idx < len(questions):
            question, answer, hint = questions[q_idx]
            st.write(f"Q{q_idx + 1}: {question}")
            user_answer = st.text_input("Your answer:", key=f"fish_{q_idx}").strip().lower()

            if user_answer:
                st.session_state.fish_attempts += 1
                if user_answer == answer:
                    st.success("Well done! You caught a fish! 🎣")
                    st.session_state.fish_caught += 1
                    st.session_state.fish_q_index += 1
                    st.session_state.fish_attempts = 0
                    st.session_state.want_hint = False
                    st.rerun()
                else:
                    st.warning("❌ Incorrect.")
                    if attempts == 2:
                        want_hint = st.radio(
                            "It looks like you are exhausted. Would you like to recharge your energy with the mocktail?",
                            options=["No", "Yes"],
                            key=f"hint_choice_{q_idx}",
                        )
                        st.session_state.want_hint = (want_hint == "Yes")
                        if st.session_state.want_hint:
                            st.info(f"Hint: {hint}")
                    if attempts >= 5:
                        st.error("You failed this question. Moving to the next one.")
                        st.session_state.fish_q_index += 1
                        st.session_state.fish_attempts = 0
                        st.session_state.fish_failed += 1
                        st.session_state.want_hint = False
                        st.rerun()

        if caught >= st.session_state.fish_goal:
            st.success("🎉 Congratulations! Hooray, YOU DID IT! 🎉")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True

# ------------------- Desert Adventure -------------------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # Level 1: Fix Boots' Song
    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.info("Hint: There are 2 incorrect words in the lyrics.")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")

        wrong_words = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])

        if set(wrong_words) == {"butt", "fein"}:
            st.success("Well done! Thank you Dora! Now Boots will help you on your journey!")
            st.session_state.progress["Desert_L1"] = True
            st.session_state.show_desert_l2 = True
            st.rerun()
        elif wrong_words:
            st.error("Not quite right. Try again!")

    # Level 2: Help Benny
    elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")
        options = ["hug", "sing", "dance", "run"]
        choice2 = st.radio("Choose one way to help:", options, key="desert2")

        if choice2:
            if choice2 == "sing":
                st.success("Well done! Boots: What a good suggestion! Let's sing! 🎵")
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                if st.session_state.desert2_fail >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.session_state.desert2_fail += 1
                st.error("Hmm… Try something else!")

        # When level 2 is done, show congratulations and balloons
        if st.session_state.progress["Desert_L2"]:
            st.success("🎉 Congratulations! You completed the Desert Adventure!")
            st.balloons()

# ------------------- Forest Adventure -------------------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]

    # Shuffle animals for difficulty
    if "forest_order" not in st.session_state:
        shuffled_indices = list(range(len(sounds)))
        random.shuffle(shuffled_indices)
        st.session_state.forest_order = shuffled_indices

    q_idx = st.session_state.forest_q_index
    if q_idx < len(sounds):
        current_index = st.session_state.forest_order[q_idx]
        sound = sounds[current_index]
        correct_animal = animals[current_index]

        options = ["pig", "bee", "cow", "cat", "rooster"]
        selected = st.selectbox(f"What animal makes this sound '{sound}'?", options, key=f"forest_{q_idx}")

        if st.button("Submit Answer", key=f"forest_submit_{q_idx}"):
            if selected == correct_animal:
                st.success("Well done! Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. The correct answer was '{correct_animal}'.")
            st.session_state.forest_q_index += 1
            st.rerun()
    else:
        st.success(f"🎉 Congratulations! You got {st.session_state.forest_score}/{len(sounds)} correct!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# ------------------- Restart button when all complete -------------------
if (
    st.session_state.progress["Beach_L2"] and
    st.session_state.progress["Desert_L2"] and
    st.session_state.progress["Forest"]
):
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()


