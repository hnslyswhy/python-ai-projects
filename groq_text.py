import os
import time
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate



load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# initialize streamlit app
st.set_page_config(page_title="Speedipedia", page_icon=":books:")
st.title("Speedipedia")
st.subheader("What do you want to know?")



# vector embedding
def vector_embedding():
    if "vectors" not in st.session_state:
        try:
            # set embedding model
            st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            # Check if file exists and show the path
            pdf_path = "./ETEC510.pdf"
            if not os.path.exists(pdf_path):
                st.error(f"PDF file not found at: {pdf_path}")
                return
            # load the pdf file--> ingest data
            st.session_state.loader = PyPDFLoader(pdf_path) 
            # load the documents
            st.session_state.docs=st.session_state.loader.load()
            if not st.session_state.docs:
                st.error("No documents were loaded from the PDF")
                return
            
            # split the documents into chunks
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
            
            if not st.session_state.final_documents:
                st.error("No text chunks were created from the documents")
                return
                
            st.session_state.vectors = FAISS.from_documents(
                st.session_state.final_documents, 
                st.session_state.embeddings
            )
            st.success("Vector store created successfully!")
            
        except Exception as e:
            st.error(f"Error creating vector store: {str(e)}")

# create UI button to trigger the vector embedding
if st.button("Create knowledge base"):
    vector_embedding()
    st.write("Knowledge base created")

# initialize llm
llm = ChatGroq(api_key=groq_api_key, model="gemma2-9b-it" )
# prompt
prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}
"""
)
user_question = st.text_input("Enter your questions:")
if user_question:
    document_chain = create_stuff_documents_chain(llm, prompt) # document chain: combines the prompt with the llm
    retriever = st.session_state.vectors.as_retriever() # retriever: retrieves the documents from the vector store
    retrieval_chain = create_retrieval_chain(retriever, document_chain) # retrieval chain: combines the retriever with the document chain
    
    start = time.process_time()
    response = retrieval_chain.invoke({"input": user_question}) # invoke the retrieval chain
    st.write(response["answer"]) 
    end = time.process_time()
    st.write(f"Time taken: {end - start:.2f} seconds")
    
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("************************************************")
        
   
   