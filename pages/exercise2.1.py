import streamlit as st
import pandas as pd
from io import StringIO
from pypdf import PdfReader
from pathlib import Path
import shutil  

st.title("Exercise 2.1")

# ===== ADDED (1): chunking function =====
def chunk_text(text, size, overlap):
    """Split text into fixed-size character chunks with overlap."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than chunk size")
    step = size - overlap
    return [text[i:i + size] for i in range(0, max(len(text) - overlap, 1), step)]
# ===== END ADDED (1) =====

# 1. Allows the user to upload a document.

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

if uploaded_file is not None:
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
        st.write(f"{len(reader.pages)} pages")
        st.text_area("Extracted text", text, height=400)


    else:  # .txt
        text = uploaded_file.getvalue().decode("utf-8", errors="replace")
        st.text_area("File contents", text, height=400)

# 2. Allows the user to chunk the document.
    st.subheader("Chunking")
    size = st.selectbox("Chunk size (characters)", [100, 1000, 10000, 100000], index=2)
    overlap_options = [o for o in [0, 50, 100, 200] if o < size]
    overlap = st.select_slider("Overlap (characters)", options=overlap_options,
                               value=min(100, overlap_options[-1]))

    if not text.strip():
        st.warning("No text could be extracted (the PDF may be scanned images).")
    else:
        chunks = chunk_text(text, size, overlap)
        st.write(f"{len(chunks)} chunks")
        for i, chunk in enumerate(chunks, 1):
            with st.expander(f"Chunk {i} ({len(chunk)} chars)"):
                st.text(chunk)

# 3. Saves each chunk of the document (to your project directory).
        PROJECT_DIR = Path(__file__).resolve().parents[1]

        if st.checkbox("Save chunks to project directory"):
            folder = st.text_input("Folder name", value=Path(uploaded_file.name).stem)
            out_dir = PROJECT_DIR / "chunks" / folder
            st.caption(f"Will save to: {out_dir}")

            all_numbers = list(range(1, len(chunks) + 1))
            if st.checkbox("Select all chunks", value=True):
                selected = all_numbers
            else:
                selected = st.multiselect(
                    "Choose chunks to save",
                    options=all_numbers,
                    format_func=lambda n: f"Chunk {n} – {chunks[n - 1][:40].strip()}…",
                )
            st.write(f"{len(selected)} of {len(chunks)} chunks selected")

            if st.button("Save chunks", disabled=not selected):
                out_dir.mkdir(parents=True, exist_ok=True)
                for old in out_dir.glob("chunk_*.txt"):
                    old.unlink()
                for n in selected:
                    (out_dir / f"chunk_{n:03}.txt").write_text(chunks[n - 1], encoding="utf-8")
                st.success(f"Saved {len(selected)} chunks to {out_dir}")

# 4. Reads the first chunk you have saved and stores it in a variable.
# 4. Reads the first chunk you have saved and stores it in a variable.
def load_saved_chunks(folder_path):
    """Return {filename: text} for every saved chunk file in a folder, in order."""
    return {f.name: f.read_text(encoding="utf-8")
            for f in sorted(folder_path.glob("chunk_*.txt"))}

st.divider()
st.subheader("Read saved chunks")

chunks_root = Path(__file__).resolve().parents[1] / "chunks"
folders = sorted(p.name for p in chunks_root.iterdir() if p.is_dir()) if chunks_root.exists() else []

if not folders:
    st.info("No saved chunks yet.")
else:
    chosen_folder = st.selectbox("Saved folder", folders)
    folder_path = chunks_root / chosen_folder            # <<< NEW LINE
    saved = load_saved_chunks(folder_path)               # <<< CHANGED (was: chunks_root / chosen_folder)

    if not saved:
        st.info("This folder has no chunk files.")
    else:
        view = st.radio("View", ["One chunk", "All chunks"], horizontal=True)
        if view == "One chunk":
            filename = st.selectbox("Chunk file", list(saved))
            st.caption(f"{len(saved[filename])} chars")
            st.text(saved[filename])
            # >>> NEW: delete the chunk being viewed
            if st.button("🗑️ Delete this chunk"):
                (folder_path / filename).unlink()
                st.rerun()
            # <<< END NEW
        else:
            for filename, content in saved.items():
                with st.expander(f"{filename} ({len(content)} chars)"):
                    st.text(content)

    # >>> NEW: delete the whole folder (4 spaces in, level with "if not saved:")
    if st.checkbox("Confirm folder deletion") and st.button(f"🗑️ Delete folder '{chosen_folder}'"):
        shutil.rmtree(folder_path)
        st.rerun()
    # <<< END NEW

# 5. Displays the first chunk back to the user.

# the above code already displays the chunks, so this requirement is satisfied by the "View" section above.
