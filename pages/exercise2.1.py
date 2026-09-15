import streamlit as st
import pandas as pd
from io import StringIO



st.title("Exercise 2.1")

# 1. Allows the user to upload a document.

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

# 2. Allows the user to chunk the document.

# 3. Saves each chunk of the document (to your project directory).

# 4. Reads the first chunk you have saved and stores it in a variable.

# 5. Displays the first chunk back to the user.
