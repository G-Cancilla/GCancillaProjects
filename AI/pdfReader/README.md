# 🧠 PDF Summarizer App

This is a simple Streamlit web app that extracts and summarizes text from PDF files. It also supports asking questions about the content using a language model.


## 🚀 Features

- 📄 Upload any PDF file
- ✂️ Automatically cleans and extracts text
- 🧠 Summarizes long documents using a pre-trained transformer
- ❓ Ask natural language questions about your document

## 🏃‍♂️ How to Run This Project
```bash
git clone https://github.com/G-Cancilla/GCancillaProjects.git
cd GCancillaProjects/AI/pdfReader

#Start python environment (if you want)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

#install the requirements for the project 
pip install -r requirements.txt

streamlit run main.py


