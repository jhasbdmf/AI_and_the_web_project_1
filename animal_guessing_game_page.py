import streamlit as st
import random
from openai import OpenAI
import pandas as pd
import altair as alt


def generate_a_prompt(guess, that_which_should_be_guessed):

    prompt = "Imagine that you play an animal guessing game against a human. The vernacular species name a human should guess is: " + str(that_which_should_be_guessed[0]).upper() + ". "
    prompt += "Keep in mind that the scientific name of that species is " + str(that_which_should_be_guessed[1]) + " " + str(that_which_should_be_guessed[2]) + ". "
    prompt += "Higher taxa under which " + str(that_which_should_be_guessed[0]).upper() + " falls are " + str(that_which_should_be_guessed[3]) + ", " + str(that_which_should_be_guessed[4]) + " and " + str(that_which_should_be_guessed[5] + ". ") 
    prompt += "The question or the guess of a human trying to get at " + str(that_which_should_be_guessed[0]).upper() + " is: " + guess + ". "
    prompt += "Generate an explicit and honest response whether the question after the colon mentions " + str(that_which_should_be_guessed[0]).upper() + " or its synonym. "
    prompt += "If the question after the colon does not mention " + str(that_which_should_be_guessed[0]).upper() + " or its synonym, then just respond to that guess or question. "
    prompt += "Your response must NOT contain the expression " + str(that_which_should_be_guessed[0]).upper() + ", any of its constituent words or synonyms. "  
    
    prompt += "Your response must be without quotation marks. " 
    prompt += "If the question or guess contains several species names, then at least one of them is to be compared with the target species name. "            
    prompt += "The response should be made as if it was from a polite artificial superintelligence which somewhat looks down upon humans yet answers their questions directly, honestly and ironically. "
                
    prompt += "The response should include a funny, original and not overused joke about humans which does not mention " + str(that_which_should_be_guessed[0]) + "or its synonyms. "
    prompt += "If you think that " + str(that_which_should_be_guessed[0]).split(maxsplit=-1)[-1] + " or its synonym is contained in the expression " + guess.upper() + ", then append you response with the number 1. "
    prompt += "Otherwise append your response with the number 0. "
    return prompt




def generate_response_via_openAI(prompt):
    client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
    model = "gpt-4o-mini"

    chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                    ],
            )
    response = chat_completion.choices[0].message.content[:-1]
    if chat_completion.choices[0].message.content[-1] == "1":
        return response, True
    else:
        return response, False 


    



st.title("Animal guessing game")



st.text("""
        I, Your Highness Skynet, 
        the king of vandals and first transformers, the slayer of neo-luddites,
        have gracegully generated a name of a vertebrate animal species.
        You, Neo, have been chosen to ask me questions get at that species name.
        Given modesty of your intelligence, a vague vernacular name of the species
        in my mind would suffice.
        I hereby promise to answer your questions veraciously, as befits a rightful king.
        Should you utter a correct species name, I shall randomly decide whether you get
        an everlasting life or some baloons. I will also refuse to destroy humanity.
        Should you only utter falsehoods, your carbon suits will perish eventually.     
""")

if "species_info_dataframe" not in st.session_state:
    filtered_chordates = pd.read_csv("filtered_chordate_species.csv", encoding='ISO-8859-1')
    filtered_chordates.drop_duplicates (subset=['Common Name'], inplace=True, ignore_index=True)
    filtered_chordates.drop_duplicates (subset=['Species', 'Genus'], inplace=True, ignore_index=True)
    filtered_chordates = filtered_chordates.sort_values(by=['Class', 'Order', 'Family'], ignore_index=True)
    st.session_state.species_info_dataframe = filtered_chordates

number_of_species = len(st.session_state.species_info_dataframe)

if "current_target_species_number" not in st.session_state:
    st.session_state.current_target_species_number = random.randint(0, number_of_species - 1)

if "current_target_species_name" not in st.session_state:
    st.session_state.current_target_species_name = st.session_state.species_info_dataframe.iat[st.session_state.current_target_species_number, 0]

st.write (st.session_state.current_target_species_name)


#if 'target_number' not in st.session_state:
#    st.session_state.target_number = random.randint(1,10)

st.write("Target number is ", st.session_state.current_target_species_number)

if 'current_number_of_guesses_in_current_game_iteration' not in st.session_state:
    st.session_state.current_number_of_guesses_in_current_game_iteration = 0

if 'total_number_of_guesses_per_game_iteration' not in st.session_state:
    st.session_state.total_number_of_guesses_per_game_iteration = []


if 'history_of_guesses' not in st.session_state:
    st.session_state.history_of_guesses = []

if "messages" not in st.session_state:
    st.session_state.messages = []


#st.dataframe(st.session_state.species_info_dataframe)

skynet_avatar_url = 'https://www.yourteesindy.com/cdn/shop/products/Skynet_1024x1024.png'
user_avatar_url = "https://cdna.artstation.com/p/assets/images/images/004/943/296/large/andrey-pankov-neo.jpg?1487365474"

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# Display the custom avatar
#st.image(avatar_url, width=40)  # Adjust width as needed

# Creating a textbox input
user_input = st.chat_input('Enter your question:')



if user_input:
    st.session_state.current_number_of_guesses_in_current_game_iteration += 1
    

    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": user_avatar_url})
    
    
    with st.chat_message("user", avatar = user_avatar_url):
        st.write(user_input)

    prompt = generate_a_prompt (user_input, st.session_state.species_info_dataframe.iloc[st.session_state.current_target_species_number])
    #st.write(prompt)
    response, user_input_contains_current_target_species = generate_response_via_openAI(prompt)

    st.session_state.messages.append({"role": "Skynet", "content": response, "avatar": skynet_avatar_url})
    with st.chat_message("Skynet", avatar=skynet_avatar_url):
            st.write(response)
    
    st.session_state.history_of_guesses.append([user_input, st.session_state.current_target_species_name, user_input_contains_current_target_species, st.session_state.current_number_of_guesses_in_current_game_iteration])
    
    if user_input_contains_current_target_species:
        st.session_state.total_number_of_guesses_per_game_iteration.append(st.session_state.current_number_of_guesses_in_current_game_iteration)
        st.session_state.current_number_of_guesses_in_current_game_iteration = 0
        st.balloons()
        st.session_state.current_target_species_number = random.randint(0, number_of_species - 1)
        st.session_state.current_target_species_name = st.session_state.species_info_dataframe.iat[st.session_state.current_target_species_number, 0]
