from pathlib import Path
import streamlit as st
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("Exercise 2.3")

##Exercise 2.3:
#1. Allows the user to ask questions of the document from Exercise 2.1.

from pathlib import Path

import streamlit as st
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



client = OpenAI()  # reads OPENAI_API_KEY from your environment
chunks_root = Path(__file__).resolve().parents[1] / "chunks"

# Setup: load the chunks saved in Exercise 2.1
folders = sorted(p.name for p in chunks_root.iterdir() if p.is_dir()) if chunks_root.exists() else []
if not folders:
    st.info("No saved chunks yet. Save some in Exercise 2.1 first.")
    st.stop()

folder = st.selectbox("Document", folders)
files = sorted((chunks_root / folder).glob("chunk_*.txt"))
chunks = [f.read_text(encoding="utf-8") for f in files]

# 1. Allows the user to ask a question of the document.
question = st.text_area("Ask a question about this document")

if question:
# 2. Retrieves the most relevant part of the document and uses this to answer the question.
# 2a. Retrieve: score every chunk against the question and keep the 3 best
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks)
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    top = scores.argsort()[::-1][:3]
    # Each chunk is labelled with its file name so the answer can cite it (supports #3)
    context = "\n\n".join(f"[{files[i].name}]\n{chunks[i]}" for i in top)

# 2b. Answer: send only the retrieved chunks, plus the question, to GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # The citation instruction here is the other half of #3
            {"role": "system", "content": "Answer using the excerpts provided. "
                                          "Cite the chunk file name for each point. "
                                          "If the answer isn't in the excerpts, say so."},
            {"role": "user", "content": f"Excerpts:\n\n{context}\n\nQuestion: {question}"},
        ],
    )

# 3. Responds to the user, citing what information was used from the document.
    # The answer itself, with inline [chunk_xxx.txt] citations
    st.write(response.choices[0].message.content)
    # The full text of the chunks that were used, so the citations can be checked
    with st.expander("Chunks used"):
        for i in top:
            st.markdown(f"**{files[i].name}**")
            st.text(chunks[i])

