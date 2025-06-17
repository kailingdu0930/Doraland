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

# ---------- MENU ----------
st.markdown("### Choose your adventure mode:")
choice = st.selectbox("Where should Dora go?", ["Beach", "Desert", "Forest"])

# ---------- BEACH ----------
if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    # --- Level 1 ---
    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Choose the ingredients that should **NOT** be included in a mocktail:")
        st.info("Hint: There are 3 alcoholic ingredients to pick.")
        ingredients = ["Sprite", "Lemon", "Ginger", "Beer", "Passion fruit", "Whisky", "Mint leaf", "Tequila"]
        selected = st.multiselect("Select alcoholic ingredients:", ingredients)
        correct = {"Beer", "Whisky", "Tequila"}
        if 0 < len(selected) < 3:
            st.warning("You selected only a few ingredients. There are more!")
        elif len(selected) == 3:
            if set(selected) == correct:
                st.success("Well done! Diego: Thanks for the help! 🍹")
                st.session_state.progress["Beach_L1"] = True
                st.rerun()
            else:
                st.error("Oops! That's not right.")

    # --- Level 2 ---
    elif not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        st.write("Dora is starving. Help her catch **5** fish!")
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
                "hint_shown": False
            }

        data = st.session_state.fish_data
        if data["caught"] < 5:
            q = questions[data["q_index"] % len(questions)]
            st.write(f"Q{data['q_index'] + 1}: {q[0]}")
            ans = st.text_input("Your answer:").strip().lower()
            if ans:
                data["attempts"] += 1
                if ans == q[1]:
                    st.success("🎣 Well done! You caught a fish!")
                    data["caught"] += 1
                    data["q_index"] += 1
                    data["attempts"] = 0
                    data["hint_shown"] = False
                    st.rerun()
                else:
                    st.warning("❌ Incorrect.")
                    if data["attempts"] == 2 and not data["hint_shown"]:
                        hint_choice = st.radio(
                            "You're exhausted. Want a mocktail to get a hint?",
                            ["No", "Yes"],
                            key=f"hint_choice_{data['q_index']}"
                        )
                        if hint_choice == "Yes":
                            st.info(f"Hint: {q[2]}")
                            data["hint_shown"] = True
                    elif data["attempts"] >= 5:
                        st.error("😓 You failed this question.")
                        data["q_index"] += 1
                        data["attempts"] = 0
                        data["hint_shown"] = False
                        st.rerun()
        else:
            st.success("🎉 Hooray, YOU DID IT!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True

# ---------- DESERT ----------
elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    # --- Level 1 ---
    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.info("Hint: There are 2 incorrect words in the lyrics.")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")
        answer = st.multiselect("Select the wrong words:", ["butt", "fein", "stream", "dream"])
        if set(answer) == {"butt", "fein"}:
            st.success("🎶 Well done! Boots: Thank you Dora!")
            st.session_state.progress["Desert_L1"] = True
            st.rerun()
        elif answer:
            st.error("Try again!")

    # --- Level 2 ---
    elif not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")
        action = st.radio("Choose one:", ["hug", "sing", "dance", "run"])
        if st.button("Submit"):
            if action == "sing":
                st.success("🎵 Well done! Benny is happy now.")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                st.rerun()
            else:
                st.error("Hmm… try something else!")

# ---------- FOREST ----------
elif choice == "Forest":
    st.header("🌲 Forest Adventure")
    st.subheader("🗺️ Animal Sound Match")
    st.write("Help Map match animals to their sounds.")
    sounds = ["oink", "buzz", "moo", "meow", "cock-a-doodle-doo"]
    correct = ["pig", "bee", "cow", "cat", "rooster"]

    if "forest_idx" not in st.session_state:
        st.session_state.forest_idx = 0
        st.session_state.forest_score = 0

    idx = st.session_state.forest_idx
    if idx < len(sounds):
        options = random.sample(correct, len(correct))
        answer = st.selectbox(f"What animal makes this sound '{sounds[idx]}'?", options, key=f"forest_{idx}")
        if st.button("Submit Answer"):
            if answer == correct[idx]:
                st.success("Well done!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was {correct[idx]}")
            st.session_state.forest_idx += 1
            st.rerun()
    else:
        st.success(f"🎉 Congratulation! You matched {st.session_state.forest_score}/5 correctly!")
        st.balloons()
        st.session_state.progress["Forest"] = True

# ---------- RESTART ----------
if all(st.session_state.progress.values()):
    st.button("🔁 Restart Adventure", on_click=lambda: st.session_state.clear())
