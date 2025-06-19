# 🧠 Smart Resume Analyser

Smart Resume Analyser is an interactive web application built using **Streamlit** that analyzes resumes (PDF format), extracts relevant information using NLP, and provides personalized recommendations for:

- Skills improvement
- Course suggestions
- Resume writing tips
- Career level identification
- Interview preparation resources

---

## 🚀 Features

- 📄 **PDF Resume Upload and Parsing**
- 🧑‍💻 **Candidate Profile Analysis** (Name, Email, Contact, Skills, etc.)
- 📊 **Skill Matching and Recommendations** for:
  - Data Science
  - Web Development
  - Android Development
  - iOS Development
  - UI/UX Design
- 🎯 **Career Level Estimation** based on resume length
- 📚 **Course and Certification Suggestions**
- 📈 **Resume Score Calculation** (based on key sections)
- 📺 **Video Recommendations** (Resume Writing & Interview Tips)

---

## 🛠️ Technologies Used

- 🐍 Python
- 📘 Streamlit
- 📄 `pyresparser` for resume parsing
- 🧠 `spaCy`, `nltk` for NLP
- 🧾 `pdfminer.six` for PDF text extraction
- 🎥 YouTube video recommendations via web scraping

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-resume-analyser.git
cd smart-resume-analyser
```

### 2. Install Dependencies

Ensure Python 3.8+ is installed. Then run:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install streamlit pyresparser pdfminer.six nltk spacy
python -m nltk.downloader stopwords punkt averaged_perceptron_tagger wordnet
python -m spacy download en_core_web_sm
```

### 3. Download NER Model

```bash
python -m spacy download en_core_web_sm
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```