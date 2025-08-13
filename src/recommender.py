# src/recommender.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Step 1: Load environment variables
load_dotenv()

# Step 2: Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 3: Initialize LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama3-8b-8192"
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["skills", "jobs"],
    template="""
You are an AI job recommendation assistant.
Given these skills: {skills}
and these job postings: {jobs}
Recommend the top 5 most suitable jobs and explain briefly why each is a good match.
"""
)

def get_recommendations(skills, jobs):
    jobs_text = "\n".join([f"{job['title']} at {job['company_name']} ({job['location']})" for job in jobs])
    prompt = prompt_template.format(skills=skills, jobs=jobs_text)
    return llm.predict(prompt)
