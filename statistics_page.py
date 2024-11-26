import streamlit as st
import pandas as pd
from openai import OpenAI


def evaluate_quality_of_a_guess_via_openAI(prompt):
    client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
  

    chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt},
                    ],
            )
    
    return chat_completion.choices[0].message.content



def find_out_whether_a_guess_applies_to_a_genus(genus, guess):
    prompt = "Does the statement {" + guess + "} apply to the genus " + genus + "? "
    prompt += "If yes, return 1. Otherwise return 0. Return nothing beying 1 or 0. "
    response = evaluate_quality_of_a_guess_via_openAI(prompt) 
    st.write (response)
    return response

#iterate through all genera and check whether a guess is true of the currently interated genus
def estimate_quality_of_a_guess(guess):
    #genera_to_which_a_guess_applies = st.session_state.genera_frequency_count["Genera"].apply(find_out_whether_a_guess_applies_to_a_genus, args = (guess,))
    #number_of_species_to_which_a_guess_applies = genera_to_which_a_guess_applies.dot(st.session_state.genera_frequency_count["Frequencies"])
    classes_to_which_a_guess_applies = st.session_state.classes_frequency_count["Classes"].apply(find_out_whether_a_guess_applies_to_a_genus, args = (guess,))
    number_of_species_to_which_a_guess_applies = classes_to_which_a_guess_applies.dot(st.session_state.classes_frequency_count["Frequencies"])
    
    quality_of_a_guess = number_of_species_to_which_a_guess_applies / len(st.session_state.st.session_state.species_info_dataframe)
    return quality_of_a_guess


st.title("Statistics")



if "current_target_species_name" in st.session_state:
    st.write (st.session_state.current_target_species_name)

if 'total_number_of_guesses_per_game_iteration' in st.session_state and len(st.session_state.total_number_of_guesses_per_game_iteration) != 0:
    mean_guesses_per_game_iteration = sum(st.session_state.total_number_of_guesses_per_game_iteration) / len(st.session_state.total_number_of_guesses_per_game_iteration)
    st.write("Average number of guesses per finished game iteration: ", mean_guesses_per_game_iteration)

    # Create a DataFrame with default index 
    number_of_guesses_per_game_iteration = pd.DataFrame(st.session_state.total_number_of_guesses_per_game_iteration, columns=['Values'])

    # Create the bar chart
    st.bar_chart(number_of_guesses_per_game_iteration)

if "species_info_dataframe" in st.session_state and "genera_frequency_count" not in st.session_state:
    st.session_state.genera_frequency_count = st.session_state.species_info_dataframe.iloc[:, 2].value_counts().reset_index()
    st.session_state.genera_frequency_count.columns = ["Genera","Frequencies"]
    st.session_state.classes_frequency_count = st.session_state.species_info_dataframe.iloc[:, 3].value_counts().reset_index()
    st.session_state.classes_frequency_count.columns = ["Classes","Frequencies"]
    #st.write(st.session_state.genera_frequency_count)
    st.write(st.session_state.classes_frequency_count)


if "history_of_guesses" in st.session_state:
    #for i in st.session_state.history_of_guesses:
        #for each guess generate an evaluation via open ai and
        # append it to each of the sublists of history_of_guesses
        

    broader_info_on_guesses = pd.DataFrame(st.session_state.history_of_guesses, columns=[
        'Guess', 'Correct species name', 'Truth value of a guess', 'Number of guesses in this game iteration'
    ])

    
    st.write(broader_info_on_guesses)
    #st.write(broader_info_on_guesses['Guess'].apply(find_out_whether_a_guess_applies_to_a_genus, args = ("Oryx",)))
    st.write(broader_info_on_guesses['Guess'].apply(estimate_quality_of_a_guess))
    



    