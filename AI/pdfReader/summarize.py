import fitz
import re


def clean_text(text):
        # Remove bullet points and special formatting characters
    text = re.sub(r"•|\u2022|- ", "", text)  # common bullets
    text = re.sub(r"\n+", " ", text)             # merge newlines
    text = re.sub(r"\s{2,}", " ", text)          # collapse extra spaces
    return text.strip()

class PDFSummarizer:
    def __init__(self, pdf_path: str, max_length: int = 1000):
        self.pdf_path = pdf_path
        self.max_length = max_length
        self.text = ""
        self.summary = ""

    def extract_text(self) -> str:
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        self.text = clean_text(text)
    
    def summarize_text(self):
        from transformers import pipeline
        summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")
        chunks = [ self.text[i:i+1000] for i in range (0 , len(self.text), 1000) ]
        for chunk in chunks:
            self.summary += summarizer(chunk)[0]['summary_text'] + '\n'
    
    def answer_question(self, question):
        from transformers import pipeline
        qa_pipeline = pipeline("question-answering")
        return qa_pipeline(question = question,  context=self.text)['answer']
    

        

