import streamlit as st

# Define your pages
pages = [
    st.Page("animal_guessing_game_page.py"),
    st.Page("statistics_page.py")
]

# Create the navigation
pg = st.navigation(pages)

try:
    # Run the selected page
    pg.run()
except Exception as e:
    # Handle errors by displaying an error message in the Streamlit app
    st.error(f"Error loading page: {e}")