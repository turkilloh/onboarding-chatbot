import os
import streamlit as st
from openai import OpenAI

api_key = os.environ.get("OPEN_AI_KEY")  # Ensure your API key is available as an environment variable
client = OpenAI(api_key=api_key)

class AIRecruiter:
    def __init__(self, client):
        self.client = client
        self.messages = [
            {"role": "system", "content": "You are Jarvis, the Recruiter is designed to act as a proactive and friendly recruiter."}
        ]
        self.question_titles = [
            "What do you like to do in your free time? Any particular hobbies or how do you usually spend your weekends?",
            "Where are you living right now?",
            "If you had to name something that truly passions you in life, what would it be?",
            "Could you describe what you do in your current role?",
            "Do you have any personal projects outside of work that you'd like to talk about?",
            "Do you prefer a job with a strict work-life balance, or would you opt for a role that demands more intensity?",
            "What do you consider your standout quality?",
            "Do you have any short-term or long-term professional goals?",
            "Do you feel confident in your English skills for daily conversations?",
            "What is your current salary, and what would be a tempting offer for you to consider switching jobs?",
            "Is there anything specific you'd like to share that could help us present you with better opportunities?"
        ]
        self.responses = {}
        self.question_index = 0

    def send_message(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        response = self.generate_response()
        self.messages.append({"role": "system", "content": response})
        return response

    def generate_response(self):
        completion = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.messages,
        )
        return completion.choices[0].message.content

# Initialize the recruiter object
recruiter = AIRecruiter(client)

# Streamlit application
st.title("Jarvis: The Network's AI Concierge")

# Initialize session state for handling the index and responses
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.responses = {}

# Display initial greeting and start interaction
if st.session_state.question_index == 0:
    st.write("Hey, I'm Jarvis, The Network's AI Concierge. I'm going to ask a few questions so we can send you curated and personalized opportunities. Shall we get started?")
    if st.button("Start"):
        st.session_state.question_index = 1

# Handle the conversation flow
if 1 <= st.session_state.question_index < len(recruiter.question_titles) + 1:
    question = recruiter.question_titles[st.session_state.question_index - 1]
    user_input = st.text_input("Please answer the question below:", key=str(st.session_state.question_index))
    if st.button("Submit Response", key=str(st.session_state.question_index)):
        if user_input:  # Ensure non-empty response
            recruiter.responses[question] = user_input
            response = recruiter.send_message(user_input)
            st.write(response)  # Display AI response
            st.session_state.question_index += 1

# Display all responses once completed
if st.session_state.question_index == len(recruiter.question_titles) + 1:
    st.success("Thank you for your responses! Here are your responses:")
    for question, answer in recruiter.responses.items():
        st.text(f"{question}: {answer}")
