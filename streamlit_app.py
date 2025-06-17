import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# Initialize progress
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

if "forest_score" not in st.session_state:
    st.session_state.forest_score = 0
if "forest_index" not in st.session_state:
    st.session_state.forest_index = 0

if "fish_data" not in st.session_state:
    st.session_state.fish_data = {
        "caught": 0,
        "q_index": 0,
        "attempts": 0,
        "failed": 0,
        "hint_choice": {}
    }

if "desert2_fail" not in st.session_state:
    st.session_state.desert2_fail = 0

# When all levels are done
if all(st.session_state.progress.values()):
    st.success("🎉 Congratulations! You completed all challenges!")
    if st.button("🔄 Restart Adventure"):
        st.session_state.clear()
        st.rerun()
else:
    # Show available levels
    choices = []
    if not st.session_state.progress["Beach_L2"]:
        choices.append("Beach")
    if not st.session_state.progress["Desert_L2"]:
        choices.append("Desert")
    if not st.session_state.progress["Forest"]:
        choices.append("Forest")

    choice = st.selectbox("Where should Dora go?", choices)

    # ---------- Beach Adventure ----------
    if choice == "Beach":
        st.header("🏖️ Beach Adventure")

        # Level 1
        if not st.session_state.progress["Beach_L1"]:
            st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
            st.write("Diego is trying to avoid alcoholic ingredients. Help him!")
            st.write("Select the ingredients that should NOT be in a mocktail:")
            st.info("Hint: There are 3 alcoholic ingredients to select.")
            ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
            selected = st.multiselect("Select alcoholic ingredients:", ingredients)

            correct_mocktail = {"Beer", "Whisky", "Tequila"}
            user_set = set(selected)

            if len(user_set) in [1, 2]:
                st.warning("You selected only a few answers, there are more!")
            elif user_set:
                if user_set == correct_mocktail:
                    st.success("Diego: Thanks Dora! Here's your mocktail! 🍹")
                    st.balloons()
                    st.session_state.progress["Beach_L1"] = True
                    st.session_state.show_beach_l2 = True
                    st.rerun()
                else:
                    st.error("Oops! Mocktails shouldn't contain alcohol. Try again!")

        # Level 2
        elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
            st.subheader("🐟 Level 2: Catching Fish")
            fish_goal = st.session_state.get("fish_goal", random.randint(1, 5))
            st.session_state.fish_goal = fish_goal
            st.write(f"Dora wants to catch **{fish_goal}** fish! Answer questions correctly to help her.")

            questions = [
                ("Which month has twenty-eight days?", "every month", "Every month has at least 28 days."),
                ("Who painted The Starry Night?", "van gogh", "A male Dutch artist."),
                ("What is the largest organ of the human body?", "skin", "It's the outermost layer of your body."),
                ("How many days are there in a year?", "365", "Think about a calendar year."),
                ("Which princess ate the poisoned apple?", "snow white", "A classic Disney princess.")
            ]

            fd = st.session_state.fish_data
            q_index = fd["q_index"]
            caught = fd["caught"]
            attempts = fd["attempts"]

            if caught >= fish_goal:
                st.success("🎉 Hooray, YOU DID IT!")
                st.balloons()
                st.session_state.progress["Beach_L2"] = True

            elif q_index < len(questions):
                question, correct, hint = questions[q_index]
                st.write(f"Q{q_index + 1}: {question}")

                answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()

                if answer:
                    fd["attempts"] += 1
                    if answer == correct:
                        st.success("🎣 You caught a fish! Moving to the next question!")
                        fd.update({
                            "caught": caught + 1,
                            "q_index": q_index + 1,
                            "attempts": 0
                        })
                        st.rerun()
                    else:
                        st.warning("❌ Incorrect.")
                        if fd["attempts"] == 2 and q_index not in fd["hint_choice"]:
                            want_hint = st.radio(
                                "You look tired. Would you like to recharge with the mocktail?",
                                ["No", "Yes"],
                                key=f"hint_choice_{q_index}"
                            )
                            fd["hint_choice"][q_index] = want_hint
                            if want_hint == "Yes":
                                st.info(f"Hint: {hint}")
                        if fd["attempts"] >= 5:
                            st.error("😓 You failed this question. Moving to the next one.")
                            fd.update({
                                "q_index": q_index + 1,
                                "attempts": 0,
                                "failed": fd["failed"] + 1
                            })
                            st.rerun()

    # ---------- Desert Adventure ----------
    elif choice == "Desert":
        st.header("🏜️ Desert Adventure")

        # Level 1
        if not st.session_state.progress["Desert_L1"]:
            st.subheader("🎵 Level 1: Fix Boots' Song")
            st.write("Boots sang the wrong words. Can you spot them?")
            st.info("Hint: There are 2 wrong words.")
            st.write("Row, row, row your butt")
            st.write("Gently down the stream")
            st.write("Merrily, merrily, merrily, merrily")
            st.write("Life is but a fein")

            desert_input = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])
            if set(desert_input) == {"butt", "fein"}:
                st.success("Thanks Dora! Boots will help you now!")
                st.balloons()
                st.session_state.progress["Desert_L1"] = True
                st.session_state.show_desert_l2 = True
                st.rerun()
            elif desert_input:
                st.error("Not quite right. Try again!")

        # Level 2
        elif st.session_state.show_desert_l2 and not st.session_state.progress["Desert_L2"]:
            st.subheader("🐂 Level 2: Help Benny")
            st.write("What can we do to help Benny feel better?")
            options = ["hug", "sing", "dance", "run"]
            choice2 = st.radio("Choose one way to help:", options, key="desert2")
            if choice2:
                if choice2 == "sing":
                    st.success("Boots: Great idea! Let's sing! 🎵")
                    st.balloons()
                    st.session_state.progress["Desert_L2"] = True
                    st.rerun()
                else:
                    if st.session_state.desert2_fail >= 2:
                        st.info("Hint: Remember level 1 knowledge.")
                    st.session_state.desert2_fail += 1
                    st.error("Try something else!")

    # ---------- Forest Adventure ----------
    elif choice == "Forest":
        st.header("🌲 Forest Adventure")
        st.subheader("🗺️ Match the Animal Sounds")

        sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
        animals = ["pig", "bee", "cow", "cat", "rooster"]

        idx = st.session_state.forest_index

        if idx >= len(sounds):
            score = st.session_state.forest_score
            st.success(f"🎉 Congratulations! You got {score}/{len(sounds)} correct!")
            st.balloons()
            st.session_state.progress["Forest"] = True
        else:
            # Shuffle options for difficulty
            options = random.sample(animals, len(animals))
            selected = st.selectbox(f"What animal makes the sound '{sounds[idx]}'?", options, key=f"forest_{idx}")
            if st.button("Submit Answer", key=f"submit_{idx}"):
                if selected == animals[idx]:
                    st.success("✅ Correct! Moving to the next one!")
                    st.session_state.forest_score += 1
                else:
                    st.error(f"❌ Wrong. The correct answer was '{animals[idx]}'")
                st.session_state.forest_index += 1
                st.rerun()
