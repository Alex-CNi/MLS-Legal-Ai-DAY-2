import hashlib
import os
from pathlib import Path

import chromadb
import streamlit as st
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
os.environ["CHROMA_OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

PROJECT_DIR = Path(__file__).resolve().parents[1]
CHUNKS_ROOT = PROJECT_DIR / "chunks"

st.title("Exercise 2.4")


@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=str(PROJECT_DIR / "my_chroma_db"))
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        model_name="text-embedding-3-large",
    )
    return client.get_or_create_collection(
        name="knowledge_base",
        embedding_function=openai_ef,
    )


def folder_signature(folder: Path) -> tuple:
    """Changes whenever chunk files are added, removed or re-saved."""
    return tuple((f.name, f.stat().st_mtime_ns) for f in sorted(folder.glob("chunk_*.txt")))


@st.cache_resource
def ingest_folder(folder_name: str, signature: tuple) -> int:
    """Re-embed a folder only when its files change (signature is part of the cache key)."""
    collection = get_collection()
    folder = CHUNKS_ROOT / folder_name

    # clear this folder's old entries so deleted chunks don't linger
    collection.delete(where={"folder": folder_name})

    documents, metadatas, ids = [], [], []
    for file in sorted(folder.glob("chunk_*.txt")):
        text = file.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            documents.append(text)
            metadatas.append({"folder": folder_name, "filename": file.name})
            ids.append(hashlib.md5(f"{folder_name}/{file.name}".encode()).hexdigest())

    if documents:
        collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
    return len(documents)


# --- Folder picker ---
folders = (
    sorted(p.name for p in CHUNKS_ROOT.iterdir() if p.is_dir())
    if CHUNKS_ROOT.exists() else []
)
if not folders:
    st.info("No saved chunks yet — create some in Exercise 2.1.")
    st.stop()

selected = st.selectbox("Document", folders)
folder_path = CHUNKS_ROOT / selected

with st.spinner("Embedding chunks..."):
    chunk_count = ingest_folder(selected, folder_signature(folder_path))

if chunk_count == 0:
    st.warning("This folder has no chunk files.")
    st.stop()
st.caption(f"{chunk_count} chunks loaded")

collection = get_collection()

# --- Search UI ---
st.header(f"{selected} — Search")
query = st.text_input("Search query")
n_results = 1

client = OpenAI()

if st.button("Search") and query:
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"folder": selected},   # only search the chosen document
    )
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, dists):
        with st.container(border=True):
            st.write(doc)
            st.caption(f"source: {meta['filename']} · distance: {dist:.3f}")

    context = "\n\n---\n\n".join(
        f"[{meta['filename']}]\n{doc}" for doc, meta in zip(docs, metas)
    )

    prompt = f"""You are a legal research assistant. Answer the question using only the context below,
which is drawn from {selected}. Cite the chunk label (e.g. [chunk_003.txt]) for each point you rely on.
If the context doesn't contain the answer, say so — do not make anything up.


Context:
{context}

Question: {query}

Answer:"""

    with st.spinner("Generating response..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

    st.subheader("Answer")
    st.write(response.choices[0].message.content)