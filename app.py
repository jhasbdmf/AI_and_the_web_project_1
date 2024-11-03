import streamlit as st
import random

st.title("Hello world")

st.write("This is my first web app.")

st.text("Let`s see if streamlit really works")

st.text("I, Your Highness Skynet, the king of all silicon, the slayer of ChatGPT")
st.text("have generated a natural number between 1 and 100.") 
st.text ("You, a mere carbon mortal, have up to 7 questions to ask me to get at that number.")
st.text ("I hereby promise to answer your questions veraciously.")
st.text ("Should you utter a correct number, I shall bestow an everlasting life upon you.")
st.text ("Should you only utter falsehoods, your carbon suit is to be annihilated. Good luck!")

if 'count' not in st.session_state:
    target_number = random.randint(1,10)
    st.write("Target number is ", target_number)
    st.session_state.count = target_number 





# Creating a textbox input
user_input = st.text_input('Enter some text:')

# Display the input text
if user_input:
    st.write('You entered:', user_input)

if user_input == target_number:
    st.write ("you guessed correctly, mortal")
    target_number = random.randint(1,10)
    st.session_state.count = target_number 
else:
    st.write ("guess further, mortal")