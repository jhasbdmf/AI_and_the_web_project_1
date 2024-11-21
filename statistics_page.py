import streamlit as st
import pandas as pd
from openai import OpenAI




def evaluate_quality_of_a_guess_via_openAI(prompt):
    client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
    model = "gpt-4o-mini"

    chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                    ],
            )
    quality_of_guess = chat_completion.choices[0].message.content.split(' ', 1)[0]
    explanation = chat_completion.choices[0].message.content.split(' ', 1)[1]
    return quality_of_guess, explanation

def generate_a_guess_quality_evalutaion_prompt(guess, target_species_name_to_guess):
    prompt = ""
 
    return prompt

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


if "history_of_guesses" in st.session_state:
    #for i in st.session_state.history_of_guesses:
        #for each guess generate an evaluation via open ai and
        # append it to each of the sublists of history_of_guesses
        

    broader_info_on_guesses = pd.DataFrame(st.session_state.history_of_guesses, columns=[
        'Guess', 'Correct species name', 'Truth value of a guess', 'Number of guesses in this game iteration'
    ])
    st.write(broader_info_on_guesses)

