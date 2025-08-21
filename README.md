# 🤖 AI-Powered Job Recommendation System using LangChain & Gemini
Streamlit web app: https://ai-job-recommendation-web-app-5cr2kzg2nwhgul4tqpcmzh.streamlit.app/
## 📌 Project Description
This project is a smart job recommendation web application built with **Python**, **Streamlit**, **LangChain**, and **Gemini API**.  
It helps users discover relevant job or internship opportunities by matching their **skills, experience, and preferences** with job listings fetched from **Google Jobs via SerpAPI**.  
The application uses **RAG (Retrieval-Augmented Generation)** techniques to generate **personalized recommendations** and explanations.

---

## ✨ Features
- 📄 Upload your **resume** (PDF/DOCX) or enter your skills manually.
- 🌍 Search for jobs in a specific **location** or job type.
- 🔍 Live job fetching from **Google Jobs (SerpAPI)**.
- 🧠 **LangChain + Gemini AI** for intelligent job matching.
- 📊 Clear, easy-to-read recommendations with explanations.
- 🖥️ **Streamlit** web interface for quick interaction.

---

## 🚀 How to Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/JatinKrRana/AI-job-recommendation-web-app.git
cd AI-job-recommendation-web-app
```

### 2️⃣ Create and activate a virtual environment
```bash
# Windows (PowerShell)
python -m venv myenv
myenv\Scripts\activate

# macOS / Linux
python3 -m venv myenv
source myenv/bin/activate
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Add environment variables
Create a .env file in the root folder and add:
```bash
SERPAPI_API_KEY=your_serpapi_api_key
GEMINI_API_KEY=your_gemini_api_key
```
### 5️⃣ Run the application
```bash
streamlit run app.py
```
## 🧾Sample Input / Output

### Input Example:

**🛠 Skills:** Python 🐍, SQL 🗃, Data Analysis 📊  
**💼 Experience:** 1️⃣ year internship in Analytics 📈  
**🌍 Location:** India 🇮🇳  
**🎯 Job Type:** Internship 📝  

**📦 Output Example:**  
```
1. Data Analyst Intern - XYZ Pvt Ltd
   📍 Location: Bengaluru, India
   💡 Why recommended: Matches your skills in Python, SQL, and Data Analysis.
   
2. Business Analyst Intern - ABC Technologies
   📍 Location: Mumbai, India
   💡 Why recommended: Relevant data interpretation skills found in your resume.
```
## 📸 Screenshots
### 🔹 Home Page
<img width="2158" height="1233" alt="Screenshot 2025-08-13 160804" src="https://github.com/user-attachments/assets/508e7908-3d6b-4a3e-8b58-c97e4a4c90a4" />

### 🔹Job Recommendations Page
<img width="2156" height="1234" alt="Screenshot 2025-08-13 160955" src="https://github.com/user-attachments/assets/a8d56f43-542b-43ff-a10a-1564bbb8ecfd" />

### 🔹AI Recommendations Page
<img width="2156" height="1230" alt="Screenshot 2025-08-13 161007" src="https://github.com/user-attachments/assets/819f8809-88e2-47ed-9344-7235e44241da" />



