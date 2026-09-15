import streamlit as st
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv


st.title("Exercise 2.2")

#1. Allows the user to copy and paste two different texts.
if "text1" not in st.session_state:
    st.session_state.text1 = ""

if "text2" not in st.session_state:
    st.session_state.text2 = ""

st.session_state.text1 = st.text_area(
    label="Text 1",
)

st.session_state.text2 = st.text_area(
    label="Text 2",
)

#2. Creates an embedding for each chunk of text. For this you will need to use the embedding function from the OpenAI API.

client = OpenAI()

st.session_state.embedding1 = client.embeddings.create(
    model="text-embedding-3-large",
    input=st.session_state.text1
)


#st.write(st.session_state.embedding1.data[0].embedding)  # This is the embedding vector for the first input text

st.session_state.embedding2 = client.embeddings.create(
    model="text-embedding-3-large",
    input=st.session_state.text2
)


#3. Displays the cosine similarity of the two embeddings.

embedding1 = np.array(st.session_state.embedding1.data[0].embedding)
embedding2 = np.array(st.session_state.embedding2.data[0].embedding)

cosine_similarity = np.dot(embedding1, embedding2) / (
    np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
)

st.write(f"Cosine similarity: {cosine_similarity:.4f}")