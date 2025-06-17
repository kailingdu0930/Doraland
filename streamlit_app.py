import streamlit as st
import random

st.set_page_config(page_title="Catch Fish with Dora", page_icon="🐟", layout="centered")

# Initialize session state
if "beach_level" not in st.session_state:
    st.session_state.beach_level = 1
    st.session_state.target_fish = random.randint(1, 5)
    st.session_state.caught_fish = 0
    st.session_state.q_index = 0
    st.session_state.attempts = 0
    st.session_state.total_failures = 0
    st.session_state.mocktail_offered = False
    st.session_state.current_question = ""
    st.session_state.current_hint = ""

questions = [
    ("Which month has twenty-eight days?", "every month", "A month with twenty-eight days doesn’t mean 'only' with twenty-eight days."),
    ("Who drew the artwork, The Starry Night?", "van gogh", "A male Dutch artist."),
    ("What is the biggest organ of the human body?", "skin", "It’s the outermost part of your body and protects everything inside."),
    ("How many days are there in a year?", "365 days", "Ask the person beside you :)"),
    ("Which of the princesses ate the poisoned apple?", "snow white", "A princess from Disney.")
]

# 🌊 Title and Dora image
st.title("🐟 Level 2: Catching Fish with Dora!")
st.image("dora.jpg", caption="Dora and Boots!", use_container_width=True)

# 🎯 Target fish
st.markdown(f"🎯 Dora is hungry and wants to catch **{st.session_state.target_fish}** fish!")
st.markdown(f"✅ Fish caught: **{st.session_state.caught_fish}** / {st.session_state.target_fish}")
st.divider()

# 🧠 Show question if game not over
if st.session_state.q_index < len(questions):
    q, correct, hint = questions[st.session_state.q_index]
    st.session_state.current_question = q
    st.session_state.current_hint = hint

    st.markdown(f"**Q{st.session_state.q_index + 1}:** {q}")
    answer = st.text_input("Your answer (try your best!):").strip().lower()

    if answer:
        if answer == correct:
            st.success("✅ Correct! You caught a fish!")
            st.session_state.caught_fish += 1
            st.session_state.q_index += 1
            st.session_state.attempts = 0
            st.session_state.mocktail_offered = False
        else:
            st.session_state.attempts += 1
            st.session_state.total_failures += 1
            st.error("❌ Incorrect answer.")

            # Diego offers a mocktail if total failures > 2 and not yet offered
            if st.session_state.total_failures > 2 and st.session_state.attempts == 2 and not st.session_state.mocktail_offered:
                st.session_state.mocktail_offered = True
                choice = st.radio("It looks like you are exhausted. Would you like to recharge with the mocktail?", ("Yes", "No"), key="mocktail_radio")
                if choice == "Yes":
                    st.info(f"🔋 Hint: {st.session_state.current_hint}")
                else:
                    st.markdown("💪 Keep trying!")

            if st.session_state.attempts >= 5:
                st.warning("😓 You failed to answer this question within 5 tries.")
                st.session_state.q_index += 1
                st.session_state.attempts = 0
                st.session_state.mocktail_offered = False

# 🎉 Game End (Success / Fail)
elif st.session_state.q_index >= len(questions):
    if st.session_state.caught_fish >= st.session_state.target_fish:
        st.success("🎉 Hooray, YOU DID IT! Dora caught all the fish she wanted!")
    else:
        st.error("😢 Oh no! Dora didn't catch enough fish. Better luck next time!")

    if st.button("🔁 Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()





