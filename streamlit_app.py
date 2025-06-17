import streamlit as st

st.set_page_config(page_title="Dora Adventure")
st.title("🗺️ Dora's Adventure Game")

# 初始化進度
if "progress" not in st.session_state:
    st.session_state.progress = {
        "Beach_L1": False,
        "Beach_L2": False,
        "Desert_L1": False,
        "Desert_L2": False,
        "Forest": False
    }

# 設定冒險模式選單（固定三個選項）
available_choices = ["Beach", "Desert", "Forest"]

# 記錄目前選擇的冒險模式
if "choice" not in st.session_state:
    st.session_state.choice = "Beach"

choice = st.selectbox("Where should Dora go?", available_choices, index=available_choices.index(st.session_state.choice))
st.session_state.choice = choice

# --- Beach Adventure ---
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

        if user_set:
            if user_set == correct_mocktail:
                st.success("Diego: Thank you Dora! Here's your mocktail! 🍹")
                st.balloons()
                st.session_state.progress["Beach_L1"] = True
                if st.button("➡️ Proceed to Beach Level 2"):
                    st.rerun()
            else:
                st.error("Oops! Mocktails shouldn't include alcohol. Try again!")

    # Level 2
    elif not st.session_state.progress["Beach_L2"]:
        st.subheader("🐟 Level 2: Catching Fish")
        st.write(f"Dora wants to catch **5** fish! Answer questions correctly to help her.")

        questions = [
            ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
            ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
            ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
            ("How many days are there in a year?", "365 days", "Ask the person beside you :)"),
            ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
        ]

        # 初始化 fish 問題狀態
        if "fish_data" not in st.session_state:
            st.session_state.fish_data = {"caught": 0, "q_index": 0, "attempts": 0, "failed": 0}

        q_index = st.session_state.fish_data["q_index"]
        caught = st.session_state.fish_data["caught"]

        if caught < 5 and q_index < len(questions):
            question, correct, hint = questions[q_index]
            st.write(f"Q: {question}")
            answer = st.text_input("Your answer:", key=f"fish_{q_index}").strip().lower()
            if answer:
                if answer == correct:
                    st.success("Correct! You caught a fish!")
                    st.session_state.fish_data["caught"] += 1
                    st.session_state.fish_data["q_index"] += 1
                    st.rerun()
                else:
                    st.error("Incorrect, try again!")
        else:
            st.success("🎉 Congrats! You caught all the fish!")
            st.balloons()
            st.session_state.progress["Beach_L2"] = True
            if st.button("➡️ Go to Desert Adventure"):
                st.rerun()

# --- Desert Adventure ---
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
            if st.button("➡️ Proceed to Desert Level 2"):
                st.rerun()
        elif desert_input:
            st.error("Not quite right. Try again!")

    elif not st.session_state.progress["Desert_L2"]:
        st.subheader("🐂 Level 2: Help Benny")
        st.write("What can we do to help Benny feel better?")

        desert2_input = st.text_input("Your suggestion:", key="desert2").strip().lower()
        correct_set = {"sing", "sing a song"}
        if desert2_input:
            if desert2_input in correct_set:
                st.success("Boots: What a good suggestion! Let's sing! 🎵")
                st.balloons()
                st.session_state.progress["Desert_L2"] = True
                if st.button("➡️ Go to Forest Adventure"):
                    st.rerun()
            else:
                if st.session_state.get("desert2_fail", 0) >= 2:
                    st.info("Hint: Use the knowledge from level 1.")
                st.session_state["desert2_fail"] = st.session_state.get("desert2_fail", 0) + 1
                st.error("Hmm… Try something else!")

# --- Forest Adventure ---
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
        answer = st.text_input(f"What animal makes this sound '{sounds[idx]}'?", key=f"forest_{idx}").strip().lower()
        if answer:
            if answer == animals[idx]:
                st.success("Correct!")
                st.session_state.forest_score += 1
            else:
                st.error(f"Wrong. It was '{animals[idx]}'")
            st.session_state.forest_index += 1
            st.rerun()
    else:
        score = st.session_state.forest_score
        st.success(f"🎉 Congrats! You got {score}/{len(sounds)} correct!")
        st.balloons()

# 重新開始按鈕
if st.button("🔄 Restart Adventure"):
    st.session_state.clear()
    st.rerun()


