import streamlit as st
from openai import OpenAI
import pandas as pd
import random
import math
import re


#this method generates a gpt-4o-mini reponse to a prompt with a desired temperature/creativity and response length
#afaik possible values of temperature are between [0, 2] where 2 would generate weird nonsense and 0 would give an uncreative but exact response

def generate_a_response_via_openAI(prompt, desired_temperature=1.1, max_response_length=200):
    #this one generates a response with given parameters
    chat_completion = st.session_state.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", 
                     "content": prompt
                    }
                ],
                temperature=desired_temperature,  
                max_tokens=max_response_length
            )
    #this one returns the best response option gpt provides to the prompt given parameters
    return chat_completion.choices[0].message.content

#this method checks whether user input via a chat is the target species to be guessed
def find_out_whether_guess_contains_target_species(guess, that_which_should_be_guessed):
    #this checks if the user gussed the common name ofthe target species
    prompt = "Does the guess contain the common name of the target species? "
    prompt += "The common mame of target species is called { " + str(that_which_should_be_guessed[0]).split(maxsplit=-1)[-1] + "}. "
    prompt += "The guess is {" + guess + "}. "
    prompt += "If the guess contains the common name of the target species, return 1. Otherwise return 0."
    response = generate_a_response_via_openAI(prompt, 0.001, 1)
    if response == "1":
        return True
    #this checks if the user gussed the scientific name ofthe target species
    prompt = "Does the guess contain the scientific name of the target species? "
    prompt += "The scientific name of that species is {" + str(that_which_should_be_guessed[1]) + " " + str(that_which_should_be_guessed[2]) + "}. "
    prompt += "The guess is {" + guess + "}. "
    prompt += "If the guess contains the scientific name of the target species, return 1. Otherwise return 0."
    response = generate_a_response_via_openAI(prompt, 0.001, 1)
    if response == "1":
        return True
    #if the user guessed neither the common nor the scientific name of the species, then his guess is incorrect
    return False

#this method given feedback to the user depending on whether he guessed the target species
def generate_a_response_to_a_guess(guess, that_which_should_be_guessed, guess_is_correct):
    
    prompt = "Imagine that you, an artificial superintelligence, play an animal guessing game against a human. "
    if guess_is_correct:
        prompt += "The human made a correct guess. Inform the human about it. "
    else:
        prompt += "The human made an incorrect guess. Inform the human about it. "
        prompt += "Also give a human a hint as to whether the guess applies to the target species. "
        prompt += "The guess is {" + guess + "}. "
        prompt += "The target species is called { " + str(that_which_should_be_guessed[0]).split(maxsplit=-1)[-1] + "}. "
        prompt += "Do not mention the target species in your response"
    prompt += "The response should be made as if it was from a polite artificial superintelligence which somewhat looks down upon humans yet answers their questions directly, honestly and ironically. "
    response = generate_a_response_via_openAI(prompt)


    return response






#Once probability of a guess is know, this method returns entropy of a guess. 
#Entropy of a guess is the metric I chose to quantify quality or goodness of a guess.
#If a guess eliminates roughly a half of the species irrespective of whether it is correct or not, then it is a good guess,
#because one can use several such guesses to arrive at the target species quickly irrespective of what the target species is.
#If a guess only eliminates a couple of species when correct or incorrect, then one might need lots of such guesses to be
#guaranteed to arrivate at the target species      
def compute_entropy_of_a_guess(probability_of_a_guess):
    if probability_of_a_guess == 0:
        return 1
    else:
        shannon_entropy = -probability_of_a_guess*math.log(probability_of_a_guess, 2) - (1-probability_of_a_guess)*math.log(1-probability_of_a_guess, 2)
        return shannon_entropy

# This GPT-authored function checks if a string is numeric.
def is_numeric(value):
    return bool(re.match(r'^\d+(\.\d+)?$', str(value)))

#this one evaluates quality of a guess with a help of the following methods
#is_numeric, compute_entropy_of_a_guess, generate_a_response_via_openAI

def estimate_quality_of_a_guess(guess):
    #one gets all taxonomic classes from which a species can be sampled
    relevant_chordate_classes = st.session_state.species_info_dataframe["Class"].unique()
    #this list will store the number of species in each class as estimated by gpt
    number_of_species_of_a_given_class = []
    #this list will store the number of species in each class of which a guess is true as estimated by gpt
    number_of_species_of_a_given_class_of_which_a_guess_is_true = []
    
    #this iterates over all relevant taxonomic classes to find out of the number
    #of species in each class of which a guess is true and the number of species in those classes
    for i in relevant_chordate_classes:
        #this one lets gpt estimate the number of species in each class
        prompt = "What is the number of " + i + " species? "
        prompt += " As a response give me just one token: the number of those species and nothing more. "
        openAI_response = generate_a_response_via_openAI(prompt, 0.01, 1)
        if not is_numeric(openAI_response):
            openAI_response = "0"
        number_of_species_of_a_given_class.append (float(openAI_response))

        #this one lets gpt estimate the number of species in each class of which the guess is true
        prompt =  "What is the number of " + i + " species of which the following guess is true? "
        prompt += "The guess is: {" + guess + "} "
        prompt += " As a response give me just one token: the number of those species and nothing more. "
        openAI_response = generate_a_response_via_openAI(prompt, 0.01, 1)
        if not is_numeric(openAI_response):
            openAI_response = "0"
        number_of_species_of_a_given_class_of_which_a_guess_is_true.append(float(openAI_response))
    
    #sanity check: number of species in a class of which a guess is true should not exceed the number of species in that class
    for i in range (min(len(number_of_species_of_a_given_class), len(number_of_species_of_a_given_class_of_which_a_guess_is_true))):
        number_of_species_of_a_given_class_of_which_a_guess_is_true[i] = min(number_of_species_of_a_given_class_of_which_a_guess_is_true[i], number_of_species_of_a_given_class[i])

    #probability of a guess is the number of species in all relevant classes of which a guess is true divided into
    #the total number of species in those classes
    probability_of_a_guess = sum(number_of_species_of_a_given_class_of_which_a_guess_is_true) / sum (number_of_species_of_a_given_class)
    #compute the entropy of a guess from its probability
    entropy_of_a_guess = compute_entropy_of_a_guess(probability_of_a_guess)
    #st.write("prob, ent ", probability_of_a_guess, entropy_of_a_guess)

    return entropy_of_a_guess



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

#initialize session variables

#this one initializes gpt
if "client" not in st.session_state:
    st.session_state.client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")


#this one reads vertebrate species of relevant classes from a preprocessed .csv file
#each row of a .csv file contains
#common name of a species
#scientific name of a species (species and genus)
#family, order, class and phylum of that species
#7 columns in total 
if "species_info_dataframe" not in st.session_state:
    filtered_chordates = pd.read_csv("filtered_chordate_species.csv", encoding='ISO-8859-1')
    #remove duplicates as judged by the common name of a species
    filtered_chordates.drop_duplicates (subset=['Common Name'], inplace=True, ignore_index=True)
    #remove duplicates as judged by the scientific name of a species (species + genus)
    filtered_chordates.drop_duplicates (subset=['Species', 'Genus'], inplace=True, ignore_index=True)
    #sort entries by 3 columns: class, order, family, so that taxonomic relatives are close
    #to one another is the table (was convenient for me while testing)
    filtered_chordates = filtered_chordates.sort_values(by=['Class', 'Order', 'Family'], ignore_index=True)
    #store info on species in a session variable
    st.session_state.species_info_dataframe = filtered_chordates

#total number of species in a dataset
number_of_species = len(st.session_state.species_info_dataframe)

if "current_target_species_number" not in st.session_state:
    #generate a random number which would correspond to a row in a species_info_dataframe
    st.session_state.current_target_species_number = random.randint(0, number_of_species - 1)

if "current_target_species_name" not in st.session_state:
    #get info on a target species to guess from a species dataframe given the value of a random variable current_target_species_number
    st.session_state.current_target_species_name = st.session_state.species_info_dataframe.iat[st.session_state.current_target_species_number, 0]

#st.write("Target number is ", st.session_state.current_target_species_number)

#this info will be displayed on the statistics page, so store in a session
if 'current_number_of_guesses_in_current_game_iteration' not in st.session_state:
    st.session_state.current_number_of_guesses_in_current_game_iteration = 0

#this info will be displayed on the statistics page, so store in a session
if 'total_number_of_guesses_per_game_iteration' not in st.session_state:
    st.session_state.total_number_of_guesses_per_game_iteration = []

#this will contain all relevant statistics for each of the guesses
if 'history_of_guesses' not in st.session_state:
    st.session_state.history_of_guesses = []

#this keeps track of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_input_enabled" not in st.session_state:
    st.session_state.chat_input_enabled = True



#pictures for the user and the machine
skynet_avatar_url = 'https://www.yourteesindy.com/cdn/shop/products/Skynet_1024x1024.png'
user_avatar_url = "https://cdna.artstation.com/p/assets/images/images/004/943/296/large/andrey-pankov-neo.jpg?1487365474"

#display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])





#give the user a chance to enter a guess
user_input = st.chat_input('Enter your question:')


#if the user enterd something, then
if user_input:
   
    st.session_state.chat_input_enabled = False
    #there is one guess more in a current game iteration 
    st.session_state.current_number_of_guesses_in_current_game_iteration += 1
    
    #push user input into message history to display it in futher runs of the page
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": user_avatar_url})
    
    
    #display user input in the current run of the page
    with st.chat_message("user", avatar = user_avatar_url):
        st.write(user_input)

   
    #check if user guessed the target species correctly
    user_input_contains_current_target_species = find_out_whether_guess_contains_target_species(user_input, st.session_state.species_info_dataframe.iloc[st.session_state.current_target_species_number])
  
    #let gpt generate a response to user input
    response_to_a_guess = generate_a_response_to_a_guess(user_input, st.session_state.species_info_dataframe.iloc[st.session_state.current_target_species_number], user_input_contains_current_target_species)
    #push the generated response to user input into message history to display it in futher runs of the page
    st.session_state.messages.append({"role": "Skynet", "content": response_to_a_guess, "avatar": skynet_avatar_url})
    #display the generated response to the user input
    with st.chat_message("Skynet", avatar=skynet_avatar_url):
            st.write(response_to_a_guess)

    #let gpt estimate the entropy and hence also quality of user guess/input
    quality_of_a_guess = estimate_quality_of_a_guess(user_input)
    #st.write("guess quality", quality_of_a_guess)
    #save info on user guess/input, target species name, whether guess is correct, number of that guess in that game iteration, entropy/quality of that guess 
    st.session_state.history_of_guesses.append([user_input, st.session_state.current_target_species_name, user_input_contains_current_target_species, st.session_state.current_number_of_guesses_in_current_game_iteration, quality_of_a_guess])
    st.session_state.chat_input_enabled = True

    #if user guessed target species correctly
    if user_input_contains_current_target_species:
        #that the number of that guess in that game iteration is the total number of guesses in that game iteration
        st.session_state.total_number_of_guesses_per_game_iteration.append(st.session_state.current_number_of_guesses_in_current_game_iteration)
        #counter of the number of guesses in a game iteration is to be set to 0
        st.session_state.current_number_of_guesses_in_current_game_iteration = 0
        #show the user that he succeded in that game iteration
        st.balloons()
        #sample a new species to guess from a species_info_dataframe
        st.session_state.current_target_species_number = random.randint(0, number_of_species - 1)
        st.session_state.current_target_species_name = st.session_state.species_info_dataframe.iat[st.session_state.current_target_species_number, 0]
