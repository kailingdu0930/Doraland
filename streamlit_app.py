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

if choice == "Beach":
    st.header("🏖️ Beach Adventure")

    if not st.session_state.progress["Beach_L1"]:
        st.subheader("🌊 Level 1: Help Diego Make a Mocktail")
        st.write("Diego is struggling to avoid alcoholic ingredients. Help him!")

        selected = st.multiselect("Select the ingredients that should NOT be included:",
                                  ["1. Sprite", "2. Lemon", "3. Ginger", "4. Beer", "5. Passion fruit",
                                   "6. Whisky", "7. Mint leaf", "8. Tequila"])

        correct_ids = {"4. Beer", "6. Whisky", "8. Tequila"}

        if selected:
            if set(selected) == correct_ids:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    elif not st.session_state.progress["Beach_L2"]:
        if st.button("Next Level →"):
            st.session_state.show_beach_L2 = True

        if st.session_state.get("show_beach_L2"):
            st.subheader("🐟 Level 2: Catching Fish")
            target_fish = st.session_state.get("target_fish", random.randint(1, 5))
            st.session_state.target_fish = target_fish

            st.write(f"Dora wants to catch **{target_fish}** fish! Answer questions correctly to help her.")

            questions = [
                ("Which month has twenty-eight days?", "every month", "All months have at least 28 days."),
                ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
                ("What is the biggest organ of the human body?", "skin", "It's your outermost layer."),
                ("How many days are there in a year?", "365 days", "Ask a calendar!"),
                ("Which of the princesses ate the poisoned apple?", "snow white", "She has seven dwarfs.")
            ]

            if "fish_data" not in st.session_state:
                st.session_state.fish_data = {
                    "caught": 0,
                    "q_index": 0,
                    "attempts": 0,
                    "failed": 0
                }

            data = st.session_state.fish_data
            if data["q_index"] < len(questions) and data["caught"] < target_fish:
                q, ans, hint = questions[data["q_index"]]
                st.write(f"Q: {q}")
                response = st.text_input("Your answer:", key="fish")

                if response:
                    response = response.strip().lower()
                    data["attempts"] += 1

                    if response == ans:
                        data["caught"] += 1
                        data["q_index"] += 1
                        data["attempts"] = 0
                        st.success(f"✅ You caught a fish! Total: {data['caught']}/{target_fish}")
                    else:
                        st.warning("❌ Incorrect.")
                        if data["attempts"] == 2:
                            st.info(f"Hint: {hint}")
                        if data["attempts"] >= 5:
                            data["q_index"] += 1
                            data["attempts"] = 0
                            st.error("😓 Skipped to next question.")

            if data["caught"] >= target_fish:
                st.success("🎉 Congratulations! Dora caught all the fish she wanted!")
                st.balloons()
                st.session_state.progress["Beach_L2"] = True

elif choice == "Desert":
    st.header("🏜️ Desert Adventure")

    if not st.session_state.progress["Desert_L1"]:
        st.subheader("🎵 Level 1: Fix Boots' Song")
        st.write("Boots sang the wrong lyrics. Can you spot the wrong words?")
        st.write("Row, row, row your butt")
        st.write("Gently down the stream")
        st.write("Merrily, merrily, merrily, merrily")
        st.write("Life is but a fein")

        lyrics_wrong = st.multiselect("Select the wrong words:",
                                      ["row", "your", "butt", "gently", "stream", "merrily", "fein"])

        if lyrics_wrong:
            if set(lyrics_wrong) == {"butt", "fein"}:
                st.success("Boots: Thanks Dora! Now I can sing properly again!")
                st.balloons()
                st.session_state.progress["Desert_L1"] = True
            else:
                st.error("❌ That's not quite right. Try again!")

    elif not st.session_state.progress["Desert_L2"]:
        if st.button("Next Level →"):
            st.session_state.show_desert_L2 = True

        if st.session_state.get("show_desert_L2"):
            st.subheader("🐂 Level 2: Help Benny")
            suggestion = st.selectbox("What can we do to help Benny feel better?",
                                      ["", "Dance", "Give food", "Sing", "Play soccer"])
            if suggestion:
                if suggestion.lower() in ["sing", "sing a song"]:
                    st.success("🎵 Boots: What a good suggestion! Let's sing together!")
                    st.balloons()
                    st.session_state.progress["Desert_L2"] = True
                else:
                    st.error("Hmm… Try something else! Hint: Think about what Boots practiced earlier.")

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
                st.success("✅ Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"❌ Oops! The correct answer is '{animals[idx]}'")
            st.session_state.forest_index += 1
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congratulations! You got {score}/{len(sounds)} correct!")
        st.balloons()

# Restart button
if st.button("🔄 Restart Adventure"):
    st.session_state.clear()



