from summarize import PDFSummarizer as pdSum
import streamlit as st
import sys


def main():
    st.title("PDF Reader")

    uploaded_file = st.file_uploader("Upload your pdf", type = "pdf")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        pdfClass = pdSum("temp.pdf")
        pdfClass.extract_text()
        
        st.subheader("Extracted Text (First 1000 Characters)")
        st.text_area("Raw Text", pdfClass.text[:1000], height = 200)
        
        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                pdfClass.summarize_text()
            st.subheader("🧠 Summary")
            st.text_area("Summary", pdfClass.summary, height = 400)

        
        question = st.text_input("Ask a question about the document")
        if question:
            with st.spinner("Answering..."):
                answer = pdfClass.answer_question(question)
            st.write("Answer: ", answer)

if __name__ == "__main__":
    main()