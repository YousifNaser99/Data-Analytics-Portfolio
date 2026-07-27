import streamlit as st


def load_style():

    st.markdown(
        """

        <style>

        /* Main Background */

        .stApp {
            background-color: #0E1117;
        }


        /* Sidebar */

        section[data-testid="stSidebar"] {

            background-color: #171B26;

        }


        section[data-testid="stSidebar"] h1 {

            color: white;

        }


        /* Titles */

        h1 {

            font-size: 42px !important;
            font-weight: 700;

        }


        h2 {

            font-weight: 600;

        }


        /* KPI Cards */

        div[data-testid="metric-container"] {

            background-color: #171B26;

            border-radius: 12px;

            padding: 15px;

            border: 1px solid #2A3040;

        }


        div[data-testid="metric-container"] label {

            color: #9CA3AF;

            font-size: 14px;

        }


        div[data-testid="metric-container"] div {

            color: white;

            font-size: 28px;

            font-weight: 700;

        }


        /* Dataframes */

        .stDataFrame {

            border-radius: 10px;

        }


        /* Buttons */

        .stButton button {

            border-radius: 8px;

            background-color: #2563EB;

            color:white;

            border:none;

        }


        .stButton button:hover {

            background-color:#1D4ED8;

        }


        </style>


        """,

        unsafe_allow_html=True
    )