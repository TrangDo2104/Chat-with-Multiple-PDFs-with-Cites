from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def get_pdf_text(pdf_docs):
    """Extracts text from a list of PDF documents.

    Parameters:
    - pdf_docs (list): A list of uploaded PDF files.

    Returns:
    - str: A concatenated string of all text extracted from the PDF documents.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """Splits text into manageable chunks for processing.

    Parameters:
    - text (str): The text to be split into chunks.

    Returns:
    - list: A list of text chunks.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks