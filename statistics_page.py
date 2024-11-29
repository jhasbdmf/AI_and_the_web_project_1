import streamlit as st
import pandas as pd
from openai import OpenAI
import math
import re


#def evaluate_quality_of_a_guess_via_openAI(prompt):
def generate_a_response_via_openAI(prompt):

    chat_completion = st.session_state.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", 
                     "content": prompt
                    }
                ],
                temperature=0.01,  
                max_tokens=1
            )
    return chat_completion.choices[0].message.content

def compute_entropy_of_a_guess(probability_of_a_guess):
    if probability_of_a_guess == 0:
        return 1
    else:
        shannon_entropy = -probability_of_a_guess*math.log(probability_of_a_guess, 2) - (1-probability_of_a_guess)*math.log(1-probability_of_a_guess, 2)
        return shannon_entropy

# This GPT-authored function checks if a string is numeric.
def is_numeric(value):
    return bool(re.match(r'^\d+(\.\d+)?$', str(value)))

def estimate_quality_of_a_guess(guess):
    relevant_chordate_classes = st.session_state.species_info_dataframe["Class"].unique()
    number_of_species_of_a_given_class = []
    number_of_species_of_a_given_class_of_which_a_guess_is_true = []
    
    for i in relevant_chordate_classes:
        prompt = "What is the number of " + i + " species? "
        prompt += " As a response give me just one token: the number of those species and nothing more. "
        openAI_response = generate_a_response_via_openAI(prompt)
        if not is_numeric(openAI_response):
            openAI_response = "0"
        number_of_species_of_a_given_class.append (float(openAI_response))

        prompt =  "What is the number of " + i + " species of which the following guess is true? "
        prompt += "The guess is: {" + guess + "} "
        prompt += " As a response give me just one token: the number of those species and nothing more. "
        openAI_response = generate_a_response_via_openAI(prompt)
        if not is_numeric(openAI_response):
            openAI_response = "0"
        number_of_species_of_a_given_class_of_which_a_guess_is_true.append(float(openAI_response))
    
    #sanity check: number of species in a class of which a guess is true should not exceed the number of species in that class
    for i in range (min(len(number_of_species_of_a_given_class), len(number_of_species_of_a_given_class_of_which_a_guess_is_true))):
        number_of_species_of_a_given_class_of_which_a_guess_is_true[i] = min(number_of_species_of_a_given_class_of_which_a_guess_is_true[i], number_of_species_of_a_given_class[i])

    probability_of_a_guess = sum(number_of_species_of_a_given_class_of_which_a_guess_is_true) / sum (number_of_species_of_a_given_class)
    entropy_of_a_guess = compute_entropy_of_a_guess(probability_of_a_guess)
    st.write("prob, ent ", probability_of_a_guess, entropy_of_a_guess)
    df = pd.DataFrame()
    df["Classes"] = relevant_chordate_classes
    df["Number_of_species"] = number_of_species_of_a_given_class
    df["Guess_is_true"] = number_of_species_of_a_given_class_of_which_a_guess_is_true
    #st.write(df)
    #st.write(number_of_species_of_a_given_class)
    #st.write(number_of_species_of_a_given_class_of_which_a_guess_is_true)
    return entropy_of_a_guess
    

def estimate_quality_of_a_guess_in_a_simple_way(guess):
    #get how classes of vertebrates and how many of those there are
    relevant_chordate_classes = st.session_state.species_info_dataframe["Class"].value_counts()
    
    
   
   
    

    number_of_species_of_a_given_class_of_which_a_guess_is_true = []
    for i in relevant_chordate_classes.to_dict():
    #for i in relevant_chordate_classes.iloc[:, 0]:
    #for i in value_counts_df.iloc[:, 0]:
        prompt = ""
        prompt += "What is the number of " + i + " species of which the following prompt is true. "
        prompt += "The prompt is: {" + guess + "} "
        prompt += " As a response give me just one token: the number of those species and nothing more. "
        openAI_response = generate_a_response_via_openAI(prompt)
        if not is_numeric(openAI_response):
            openAI_response = "2"
        number_of_species_of_a_given_class_of_which_a_guess_is_true.append(openAI_response)
        #st.write(i, generate_a_response_via_openAI(prompt))

       # relevant_chordate_classes["Count of species of which a guess is true"].append(generate_a_response_via_openAI(prompt))
    
    value_counts_df = st.session_state.species_info_dataframe.groupby('Class').size().reset_index(name='Count')
    value_counts_df["guess_is_true"] = number_of_species_of_a_given_class_of_which_a_guess_is_true
    value_counts_df['Count'] = pd.to_numeric(value_counts_df['Count'], errors='coerce')
    value_counts_df['guess_is_true'] = pd.to_numeric(value_counts_df['guess_is_true'], errors='coerce')
    st.write(value_counts_df)
    number_of_species_of_which_a_guess_is_true = value_counts_df['Count'].dot(value_counts_df["guess_is_true"])
    st.write(number_of_species_of_which_a_guess_is_true)
    #probability_of_a_guess = int(number_of_species_of_which_a_guess_is_true)/len(st.session_state.species_info_dataframe)
    #retutn (compute_entropy_of_a_guess(probability_of_a_guess))

    

    #prompt = "What is the percentage of mammals of which the following prompt is true. "
    #prompt += "The prompt is: {" + guess + "} "
    #prompt += " As a response give me just one token: percentage as a numeric value between 0 and 1 and nothing more "
    #probability_of_a_guess = generate_a_response_via_openAI(prompt)
    #st.write(prompt, probability_of_a_guess)
    #quality_of_a_guess = compute_entropy_of_a_guess(float(probability_of_a_guess))
    #return quality_of_a_guess


st.title("Statistics page")


if "client" not in st.session_state:
    st.session_state.client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
  

if "current_target_species_name" in st.session_state:
    st.write (st.session_state.current_target_species_name)

if 'total_number_of_guesses_per_game_iteration' in st.session_state and len(st.session_state.total_number_of_guesses_per_game_iteration) != 0:
    mean_guesses_per_game_iteration = sum(st.session_state.total_number_of_guesses_per_game_iteration) / len(st.session_state.total_number_of_guesses_per_game_iteration)
    st.write("Average number of guesses per finished game iteration: ", mean_guesses_per_game_iteration)

    # Create a DataFrame with default index 
    number_of_guesses_per_game_iteration = pd.DataFrame(st.session_state.total_number_of_guesses_per_game_iteration, columns=['Values'])

    # Create the bar chart
    st.bar_chart(number_of_guesses_per_game_iteration)




if "history_of_guesses" in st.session_state:

    broader_info_on_guesses = pd.DataFrame(st.session_state.history_of_guesses, columns=[
        'Guess', 'Correct species name', 'Truth value of a guess', 'Number of guesses in this game iteration'
    ])

    st.write(st.session_state.species_info_dataframe["Class"].value_counts())
    st.write(broader_info_on_guesses)
    st.write(broader_info_on_guesses['Guess'].apply(estimate_quality_of_a_guess))