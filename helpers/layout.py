import streamlit as st
import helpers.constants as constants

def reduce_spacing():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_header():
    st.markdown(f"<h1 style='text-align: center; margin-bottom: 1rem;'>{constants.TITLE}</h1>", unsafe_allow_html=True)