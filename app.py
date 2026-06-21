import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🎯 AI Interview Coach")
st.subheader("Practice interviews and get AI feedback!")

job_role = st.text_input("Enter the job role you're applying for:",
                          placeholder="e.g. Python Developer")

if st.button("Generate Questions") and job_role:
    with st.spinner("Generating questions..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", 
                       "content": f"Generate 5 interview questions for a {job_role} role. Number them 1-5."}]
        )
        st.session_state.questions = response.choices[0].message.content
        st.session_state.job_role = job_role

if "questions" in st.session_state:
    st.markdown("### 📋 Your Interview Questions")
    st.write(st.session_state.questions)

    st.markdown("### ✍️ Your Answer")
    question_num = st.selectbox("Select question to answer:", [1,2,3,4,5])
    user_answer = st.text_area("Type your answer here:")

    if st.button("Get AI Feedback") and user_answer:
        with st.spinner("Analyzing your answer..."):
            feedback = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": f"""
                Job Role: {st.session_state.job_role}
                Interview Question #{question_num}
                Candidate Answer: {user_answer}

                Give feedback in this format:
                ✅ What was good:
                ⚠️ What to improve:
                ⭐ Score out of 10:
                💡 Better answer tip:
                """}]
            )
            st.markdown("### 🤖 AI Feedback")
            st.write(feedback.choices[0].message.content)
