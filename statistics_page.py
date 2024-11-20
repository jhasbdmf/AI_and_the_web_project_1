import streamlit as st

st.title("Statistics")

if "target_species_name" in st.session_state:
    st.write (st.session_state.target_species_name)


if "history_of_guesses" in st.session_state:
    st.write(st.session_state.history_of_guesses)