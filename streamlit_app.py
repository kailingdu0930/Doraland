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

st.markdown("### Choose your adventure mode:")
choice = st.selectbox("Where should Dora go?", ["", "Beach", "Desert", "Forest"])

# ---------- BEACH ----------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # LEVEL 1
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Diego is struggling to avoid alcoholic ingredients. Help him choose the right ones!")

        options = [
            "1. Sprite",
            "2. Lemon",
            "3. Ginger",
            "4. Beer",
            "5. Passion fruit",
            "6. Whisky",
            "7. Mint leaf",
            "8. Tequila"
        ]

        selected = st.multiselect(
            "❌ Select the ingredients that should NOT be in a mocktail:",
            options
        )

        correct_set = {"4. Beer", "6. Whisky", "8. Tequila"}

        if set(selected) == correct_set:
            st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
            st.balloons()
            st.session_state.progress["Beach_L1"] = True
            st.rerun()
        elif selected:
            st.error("Oops! That's not quite right. Try again!")

    # LEVEL 2
    elif not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        target_fish = st.session_state.get("target_fish", random.randint(1, 5))
        st.session_state.target_fish = target_fish

        st.write(f"Dora wants to catch **{target_fish}** fish! Answer questions correctly to help her.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "All months have at least 28 days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body."),
            ("How many days are there in a year?", "365", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        if "fish_data" not in st.session_state:
            st.session_state.fish_data = {
                "caught": 0,
                "q_index": 0,
                "attempts": 0,
                "failed": 0
            }

        q_index = st.session_state.fish_data["q_index"]
        caught = st.session_state.fish_data["caught"]

        if q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q: {question}")
            answer = st.text_input("Your answer:").strip().lower()

            if answer:
                st.session_state.fish_data["attempts"] += 1
                if answer == correct:
                    caught += 1
                    st.session_state.fish_data.update({
                        "caught": caught,
                        "attempts": 0,
                        "q_index": q_index + 1
                    })
                    st.success(f"You caught a fish! Total: {caught}/{target_fish}")
                else:
                    st.warning("❌ Incorrect.")
                    if st.session_state.fish_data["attempts"] == 2 and st.session_state.fish_data["failed"] > 2:
                        if st.button("I'm tired! Recharge with a mocktail?"):
                            st.info(f"🔋 Hint: {hint}")
                    if st.session_state.fish_data["attempts"] >= 5:
                        st.session_state.fish_data["q_index"] += 1
                        st.session_state.fish_data["attempts"] = 0
                        st.session_state.fish_data["failed"] += 1
                        st.error("😓 You failed this question.")
        else:
            if caught >= target_fish:
                st.success("🎉 Hooray, YOU DID IT! Dora caught all the fish she wanted!")
                st.balloons()
                st.session_state.progress["Beach_L2"] = True

# ---------- DESERT ----------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")

        desert_input = st.text_input("Type the wrong words (comma separated):").strip().lower()
        if desert_input:
            user_set = set([x.strip() for x in desert_input.split(",")])
            if user_set == {"butt", "fein"}:
                st.success("Thank you Dora! Now Boots will help you on your journey!")
                st.balloons()
                st.session_state.progress["Desert_L1"] = True
                st.rerun()
            else:
                st.error("Not quite right. Try again!")

    elif not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")

        desert2_input = st.text_input("Your suggestion:").strip().lower()
        correct_set = {"sing", "sing a song"}
        if desert2_input:
            if desert2_input in correct_set:
                st.success("Boots: What a good suggestion! Let's sing! 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
            else:
                if st.session_state.get("desert2_fail", 0) >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.session_state["desert2_fail"] = st.session_state.get("desert2_fail", 0) + 1
                st.error("Hmm… Try something else!")

# ---------- FOREST ----------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")

    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    animals = ["pig", "bee", "cow", "cat", "chicken"]

    if "forest_score" not in st.session_state:
        st.session_state.forest_score = 0
        st.session_state.forest_index = 0

    idx = st.session_state.forest_index
    if idx < len(sounds):
        answer = st.text_input(f"What animal makes this sound '{sounds[idx]}'?").strip().lower()
        if answer:
            if answer == animals[idx]:
                st.success("Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was '{animals[idx]}'")
            st.session_state.forest_index += 1
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulations! You got {score}/{len(sounds)} correct!")
        st.balloons()

# ---------- RESET BUTTON ----------
if st.button("🔄 Restart Adventure"):
    st.session_state.clear()
    st.rerun()





