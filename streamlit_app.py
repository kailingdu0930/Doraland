import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure Game")
st.title("🗺️ Dora's Adventure Game")

# Initialize game progress
if "progress" not in st.session_state:
    st.session_state.progress = {
        "Beach_L1": False,
        "Beach_L2": False,
        "Desert_L1": False,
        "Desert_L2": False,
        "Forest": False
    }

# Initialize other states
if "beach_show_level2" not in st.session_state:
    st.session_state.beach_show_level2 = False
if "desert_show_level2" not in st.session_state:
    st.session_state.desert_show_level2 = False

# Select available adventures based on progress
available_choices = []
if not st.session_state.progress["Beach_L1"] or (st.session_state.progress["Beach_L1"] and not st.session_state.progress["Beach_L2"]):
    available_choices.append("Beach")
if not st.session_state.progress["Desert_L1"] or (st.session_state.progress["Desert_L1"] and not st.session_state.progress["Desert_L2"]):
    available_choices.append("Desert")
if not st.session_state.progress["Forest"]:
    available_choices.append("Forest")

if len(available_choices) == 0:
    st.success("🎉 Congratulations! You have completed all adventures!")
    if st.button("Restart Adventure"):
        st.session_state.clear()
        st.rerun()
    st.stop()

choice = st.selectbox("Choose Dora's adventure:", available_choices)

# ========== BEACH ADVENTURE ==========
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # Level 1: Choose alcoholic ingredients
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("Level 1: Help Diego avoid alcohol!")
        st.write("Choose all alcoholic ingredients (3 total):")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)

        correct_set = {"Beer", "Whisky", "Tequila"}

        if len(selected) in [1, 2]:
            st.warning("You selected less than 3. There are more alcoholic ingredients.")
        elif set(selected) == correct_set:
            st.success("Correct! Diego can now make a proper mocktail!")
            st.balloons()
            st.session_state.progress["Beach_L1"] = True
            st.session_state.beach_show_level2 = True
            st.rerun()
        elif len(selected) > 0:
            st.error("Incorrect selection. Try again!")

    # Level 2: Fish catching game
    elif st.session_state.beach_show_level2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("Level 2: Help Dora catch fish!")

        # Fish goal random 1-5 stored in session_state
        if "fish_goal" not in st.session_state:
            st.session_state.fish_goal = random.randint(1, 5)
            st.session_state.fish_caught = 0
            st.session_state.fish_q_index = 0
            st.session_state.fish_attempts = 0
            st.session_state.fish_failed = 0
            st.session_state.fish_hint_asked = False

        fish_goal = st.session_state.fish_goal
        fish_caught = st.session_state.fish_caught
        q_index = st.session_state.fish_q_index
        attempts = st.session_state.fish_attempts
        failed = st.session_state.fish_failed
        hint_asked = st.session_state.fish_hint_asked

        st.write(f"Dora wants to catch **{fish_goal}** fish. Each correct answer catches one fish.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean “only” with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        # Finished catching enough fish?
        if fish_caught >= fish_goal:
            st.success("🎉 Congratulations! Hooray, YOU DID IT!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True
            st.rerun()

        # Finished all questions but not enough fish
        elif q_index >= len(questions):
            st.warning("You've answered all questions but didn't catch enough fish.")
            if st.button("Restart Level 2"):
                for key in ["fish_goal", "fish_caught", "fish_q_index", "fish_attempts", "fish_failed", "fish_hint_asked"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

        else:
            question, correct_ans, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key="fish_answer").strip().lower()

            if answer:
                attempts += 1
                st.session_state.fish_attempts = attempts

                if answer == correct_ans:
                    st.success("Correct! You caught a fish!")
                    st.balloons()
                    fish_caught += 1
                    q_index += 1
                    attempts = 0
                    failed = 0
                    hint_asked = False

                    # Update states
                    st.session_state.fish_caught = fish_caught
                    st.session_state.fish_q_index = q_index
                    st.session_state.fish_attempts = attempts
                    st.session_state.fish_failed = failed
                    st.session_state.fish_hint_asked = hint_asked

                    st.rerun()

                else:
                    st.error("Incorrect answer.")

                    if attempts >= 2 and not hint_asked:
                        want_hint = st.radio("It looks like you are exhausted. Would you like to recharge your energy with the mocktail?", ("No", "Yes"), key="mocktail_hint")
                        if want_hint == "Yes":
                            st.info(f"Hint: {hint}")
                        st.session_state.fish_hint_asked = True

                    if attempts >= 5:
                        st.warning("You failed this question. Moving to the next one.")
                        q_index += 1
                        attempts = 0
                        failed += 1
                        hint_asked = False

                        st.session_state.fish_q_index = q_index
                        st.session_state.fish_attempts = attempts
                        st.session_state.fish_failed = failed
                        st.session_state.fish_hint_asked = hint_asked

                        st.rerun()

# ========== DESERT ADVENTURE ==========
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # Level 1
    if not st.session_state.progress["Desert_L1"]:
        st.subheader("Level 1: Fix Boots' Song")
        st.write("Select the wrong words Boots sang (2 wrong words):")
        st.write('"Row, row, row your butt"')
        st.write('"Gently down the stream"')
        st.write('"Merrily, merrily, merrily, merrily"')
        st.write('"Life is but a fein"')

        wrong_words = ["butt", "fein", "stream", "dream"]
        selected = st.multiselect("Choose wrong words:", wrong_words)
        if set(selected) == {"butt", "fein"}:
            st.success("Correct! Boots can now help Dora!")
            st.balloons()
            st.session_state.progress["Desert_L1"] = True
            st.session_state.desert_show_level2 = True
            st.rerun()
        elif len(selected) > 0:
            st.error("Incorrect selection. Try again!")

    # Level 2
    elif st.session_state.desert_show_level2 and not st.session_state.progress["Desert_L2"]:
        st.subheader("Level 2: Help Benny")

        if "desert2_attempts" not in st.session_state:
            st.session_state.desert2_attempts = 0
            st.session_state.desert2_hint_given = False

        st.write("Choose one way to help Benny feel better:")

        options = ["hug", "sing", "dance", "run"]
        choice2 = st.radio("Your choice:", options, key="desert2_choice")

        if choice2:
            if choice2 == "sing":
                st.success("Correct! Singing helps Benny feel better!")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                st.session_state.desert2_attempts += 1
                attempts = st.session_state.desert2_attempts
                st.error("Wrong choice. Try again!")

                if attempts >= 2 and not st.session_state.desert2_hint_given:
                    want_hint = st.radio("You seem tired. Want to drink the mocktail for a hint?", ("No", "Yes"), key="desert2_hint")
                    if want_hint == "Yes":
                        st.info("Hint: Think about what Boots suggested in Level 1!")
                    st.session_state.desert2_hint_given = True

# ========== FOREST ADVENTURE ==========
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("Animal Sound Match")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "rooster"]

    if "forest_q_index" not in st.session_state:
        st.session_state.forest_q_index = 0
        st.session_state.forest_score = 0

    idx = st.session_state.forest_q_index

    if idx < len(sounds):
        sound = sounds[idx]
        correct_animal = animals[idx]

        # Prepare randomized options
        options = animals.copy()
        random.shuffle(options)

        answer = st.selectbox(f"What animal makes this sound: '{sound}'?", options, key="forest_select")

        if st.button("Submit Answer", key="forest_submit"):
            if answer == correct_animal:
                st.success("Correct!")
                st.balloons()
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong! The correct answer is '{correct_animal}'.")
            st.session_state.forest_q_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulations! You scored {score} out of {len(sounds)}!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# Restart all if done
if all(st.session_state.progress.values()):
    if st.button("Restart Game"):
        st.session_state.clear()
        st.rerun()


