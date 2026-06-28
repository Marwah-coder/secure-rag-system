from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 1: PDF se text extract karo
def load_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

# Step 2: Text ko chunks mein todo
def split_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # har chunk mein roughly 500 characters
        chunk_overlap=50,    # chunks ke beech 50 character ka overlap (context na toote)
        separators=["\n\n", "\n", ". ", " "]  # pehle paragraph, phir line, phir sentence se todo
    )
    chunks = splitter.split_text(text)
    return chunks

if __name__ == "__main__":
    text = load_pdf("documents/company_handbook.pdf")
    print(f"Total characters extracted: {len(text)}")

    chunks = split_into_chunks(text)
    print(f"Total chunks created: {len(chunks)}")
    print("\n--- First chunk sample ---")
    print(chunks[0])
    print("\n--- Second chunk sample ---")
    print(chunks[1])