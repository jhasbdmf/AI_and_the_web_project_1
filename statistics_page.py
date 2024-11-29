import streamlit as st
import pandas as pd
from openai import OpenAI
import math
import re


st.title("Statistics page")


#if "client" not in st.session_state:
#    st.session_state.client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
  

#if "current_target_species_name" in st.session_state:
#    st.write (st.session_state.current_target_species_name)

#compute and disply average number of guesses per iteration if there is at least one successful guess
if 'total_number_of_guesses_per_game_iteration' in st.session_state and len(st.session_state.total_number_of_guesses_per_game_iteration) != 0:
    mean_guesses_per_game_iteration = sum(st.session_state.total_number_of_guesses_per_game_iteration) / len(st.session_state.total_number_of_guesses_per_game_iteration)
    st.write("Average number of guesses per finished game iteration: ", mean_guesses_per_game_iteration)

    
    # Create a DataFrame with stores the number of guesses per game iteration 
    number_of_guesses_per_game_iteration = pd.DataFrame(st.session_state.total_number_of_guesses_per_game_iteration, columns=['Values'])

    #display a that dataframe as a bar chart
    st.bar_chart(number_of_guesses_per_game_iteration)
    




if "history_of_guesses" in st.session_state:

    st.write("""
        Entropy of a guess is the metric chosen to quantify quality or goodness of a guess.
        If a guess eliminates roughly a half of animal species irrespective of whether it is correct or not, then it is a good guess,
        because one can use several such guesses to arrive at the target species quickly irrespective of what the target species is.
        If a guess only eliminates a couple of species when correct or incorrect, then one might need lots of such guesses to be
        guaranteed to arrivate at the target species  
    """)
    #store broader info on guesses in a dataframe
    broader_info_on_guesses = pd.DataFrame(st.session_state.history_of_guesses, columns=[
        'Guess', 'Correct species name', 'Truth value of a guess', 'Guess per iteration', 'Estimated guess quality'
    ])

    #display that dataframe
    st.write(broader_info_on_guesses)
  