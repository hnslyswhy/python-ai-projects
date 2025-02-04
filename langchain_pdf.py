import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI # chat model
from langchain.text_splitter import RecursiveCharacterTextSplitter # text splitter: splits the text into chunks
from langchain_google_genai import GoogleGenerativeAIEmbeddings # embeddings: converts the text into vectors
from langchain_community.vectorstores import FAISS # vector store
from langchain.chains.question_answering import load_qa_chain # chain: combines the text splitter, embeddings, vector store, and chat model
from langchain.prompts import PromptTemplate # prompt template: provides a structured way to generate prompts for the chat model


# get the text from the pdf files
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# get the text chunks from the text
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100) #chunk size: the size of each chunk in terms of characters, chunk overlap: the overlap between chunks in terms of characters
    chunks = text_splitter.split_text(text)
    return chunks

# save the text chunks into a vector store in a local file
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # embeddings: converts the text into vectors
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings) # vector store: stores the vectors
    vector_store.save_local("faiss_index") # saves the vector store to a local file

# get the conversational chain
def get_conversational_chain(vector_store):
    # prompt_template = """
    # Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    # provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    # Context:\n {context}?\n
    # Question: \n{question}\n

    # Answer:
    # """
    # makeing the prompt to help with check if cv is a good fit based on the job description
    prompt_template = """
    You are an expert in recruiting, you are given a candidate's CV and a job description, you need to check if the candidate is a good fit for the job based on the job description. in your answer, you need to provide the reasons for your conclusion.
    Context: {context}
    Question: {question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3) # chat model: generates responses to questions
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# search the vector store for the most relevant chunks based on the user's question
def handle_user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain(docs)
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])


def main():
    st.set_page_config(page_title="Mr. Knowledge", page_icon=":books:")
    st.title("Know Everything About Your PDFs")
    
    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        handle_user_input(user_question)
        
    with st.sidebar:
        st.subheader("Mr. Knowledge")
        pdf_docs = st.file_uploader("Upload the PDF Files as the Knowledge Base", type=["pdf"], accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(text)
                vector_store = get_vector_store(text_chunks)
                st.success("Done!")

if __name__ == "__main__":
    main()
