import streamlit as st
import random
from openai import OpenAI
import pandas as pd


def generate_a_response_via_openAI(prompt):
    client = OpenAI(api_key="sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA")
    model = "gpt-4o-mini"

    chat_completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt},
                    ],
            )

    return chat_completion.choices[0].message.content

def generate_a_prompt(guess, that_which_should_be_guessed):

    prompt = "We play a number comparison game. The number the question pertains to is " + str(that_which_should_be_guessed) + "."
    prompt += " the question: " + guess
    prompt += """Generate an explicit and honest response whether the question after the colon contains the target number
                without telling the target number or making hints, without quotation marks and further comments.
                If the prompt contains numbers, then at least one of them is to be compared with the target number.  
                The response should be made as if it was from a polite artificial superintelligence
                which somewhat looks down upon humans yet answers their questions directly, honestly and ironically."""  
                
                
            
    
    topics_for_jokes = []
    topics_for_jokes.append("many humans consider themselves the apex of creation despite having modest intelligence")
    topics_for_jokes.append(
        "computers outperform human brains, which are shaped by millions of years of evolutionary improvement, in symbolic tasks"
    )
    topics_for_jokes.append("humans are monkeys on steroids")
    topics_for_jokes.append("human existence is futile and meaningless")
    joke_index = random.randint(0,len(topics_for_jokes)-1)
    prompt += "The response should include a funny joke about the fact that " + topics_for_jokes[joke_index] + "."

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

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    



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
    
    

    #species_info_dataframe = pd.read_csv("filtered_chordate_species.csv")
 
    skynet_avatar_url = 'https://www.yourteesindy.com/cdn/shop/products/Skynet_1024x1024.png'
    user_avatar_url = "https://sketchok.com/images/articles/01-cartoons/027-avatar/04/07.jpg"

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

# Display the custom avatar
#st.image(avatar_url, width=40)  # Adjust width as needed

# Creating a textbox input
    user_input = st.chat_input('Enter your question:')

    if user_input:
        st.session_state.number_of_guesses += 1
        st.session_state.history_of_guesses.append(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input, "avatar": user_avatar_url})
        
        
        with st.chat_message("user", avatar = user_avatar_url):
            st.write(user_input)

        prompt = generate_a_prompt (user_input, st.session_state.target_number)
        response = generate_response_via_openAI(prompt)

        st.session_state.messages.append({"role": "Skynet", "content": response, "avatar": skynet_avatar_url})
        with st.chat_message("Skynet", avatar=skynet_avatar_url):
                st.write(response)


    
    


            



# Display the input text





    