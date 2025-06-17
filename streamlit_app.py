import streamlit as st
import random

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

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

available_choices = [""]
if not st.session_state.progress["Beach_L1"]:
    available_choices.append("Beach")
elif not st.session_state.progress["Beach_L2"]:
    available_choices.append("Beach")
elif not st.session_state.progress["Desert_L1"]:
    available_choices.append("Desert")
elif not st.session_state.progress["Desert_L2"]:
    available_choices.append("Desert")
elif not st.session_state.progress["Forest"]:
    available_choices.append("Forest")

choice = st.selectbox("Where should Dora go?", available_choices)

# -------------- Beach Adventure --------------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

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
            st.warning("你只選了幾個答案，還有其他答案喔～")
        elif user_set:
            if user_set == correct_mocktail:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                st.session_state.show_beach_l2 = True
                st.experimental_rerun()
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    elif st.session_state.show_beach_l2 and not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        fish_goal = st.session_state.get("fish_goal", random.randint(1, 5))
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
                "hint_choice": {}
            }

        q_index = st.session_state.fish_data["q_index"]
        caught = st.session_state.fish_data["caught"]
        attempts = st.session_state.fish_data["attempts"]

        if caught < fish_goal and q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q{q_index + 1}: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()
            if answer:
                st.session_state.fish_data["attempts"] += 1
                if answer == correct:
                    st.success("🎣 You caught a fish!")
                    st.session_state.fish_data.update({
                        "caught": caught + 1,
                        "q_index": q_index + 1,
                        "attempts": 0
                    })
                    st.rerun()
                else:
                    st.warning("❌ Incorrect.")
                    if st.session_state.fish_data["attempts"] == 2:
                        want_hint = st.radio("It looks like you are exhausted. Would you like to recharge your energy with the mocktail?", ["No", "Yes"], key=f"hint_choice_{q_index}")
                        st.session_state.fish_data["hint_choice"][q_index] = want_hint
                        if want_hint == "Yes":
                            st.info(f"Hint: {hint}")
                    if st.session_state.fish_data["attempts"] >= 5:
                        st.session_state.fish_data.update({
                            "q_index": q_index + 1,
                            "attempts": 0,
                            "failed": st.session_state.fish_data["failed"] + 1
                        })
                        st.error("😓 You failed this question.")
                        st.rerun()

        if caught >= fish_goal:
            st.success("🎉 Hooray, YOU DID IT!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True

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
        choice = st.radio("Choose one way to help:", options, key="desert2")
        if choice:
            if choice == "sing":
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
        choices = ["pig", "bee", "cow", "cat", "rooster"]
        answer = st.radio(f"What animal makes this sound '{sounds[idx]}'?", choices, key=f"forest_{idx}")
        if st.button("Submit Answer", key=f"submit_{idx}"):
            if answer == animals[idx]:
                st.success("Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was '{animals[idx]}'")
            st.session_state.forest_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulation! You got {score}/{len(sounds)} correct!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# Restart button
if st.session_state.progress["Beach_L2"] and st.session_state.progress["Desert_L2"] and st.session_state.progress["Forest"]:
    st.button("🔄 Restart Adventure", on_click=lambda: st.session_state.clear())
