import streamlit as st
import random

st.title("Guessing game")


st.text("I, Your Highness Skynet, ")
st.text("the king of vandals and first computers, the slayer of ChatGPT,") 
st.text("have gracegully generated a natural number between 1 and 33.") 
st.text ("You, a mere carbon mortal, have up to 7 questions to ask me to get at that number.")
st.text ("I hereby promise to answer your questions veraciously, as befits a rightful king.")
st.text ("Should you utter a correct number, I shall bestow an everlasting life upon you.")
st.text ("Should you only utter falsehoods, your carbon suit is to be annihilated.")
st.text ("")




if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1,10)

st.write("Target number is ", st.session_state.target_number)

if 'number_of_guesses' not in st.session_state:
    st.session_state.number_of_guesses = 0

if 'history_of_guesses' not in st.session_state:
    st.session_state.history_of_guesses = []

if "messages" not in st.session_state:
    st.session_state.messages = []
 
skynet_avatar_url = 'https://www.yourteesindy.com/cdn/shop/products/Skynet_1024x1024.png'
user_avatar_url = "https://sketchok.com/images/articles/01-cartoons/027-avatar/04/07.jpg"

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# Display the custom avatar
#st.image(avatar_url, width=40)  # Adjust width as needed

# Creating a textbox input
user_input = st.chat_input('Enter your guess:')

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": user_avatar_url})
    st.session_state.number_of_guesses += 1
    #st.write("Number of guesses ", st.session_state.number_of_guesses)
    with st.chat_message("user", avatar = user_avatar_url):
        st.write(user_input)
    st.session_state.history_of_guesses.append(user_input)
    #st.write("History of guesses", st.session_state.history_of_guesses)
    if user_input == str(st.session_state.target_number):
        st.session_state.messages.append({"role": "Skynet", "content": "you guessed correctly, mortal", "avatar": user_avatar_url})
        with st.chat_message("Skynet", avatar=skynet_avatar_url):
            st.write("you guessed correctly, mortal")
        st.session_state.number_of_guesses = 0
        st.session_state.history_of_guesses = []
        st.session_state.target_number = random.randint(1,10)
    else:
        #st.write ("guess further, mortal")
        st.session_state.messages.append({"role": "Skynet", "content": "guess further, mortal", "avatar": skynet_avatar_url})
        with st.chat_message("Skynet", avatar=skynet_avatar_url):
            st.write("guess further, mortal")



# Display the input text





    