import streamlit as st
from pages.minutes.main import minutes_page

def main():
    st.set_page_config(
        page_title="Label",
        page_icon="🏷️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    minutes_page()

if __name__ == "__main__":
    main()