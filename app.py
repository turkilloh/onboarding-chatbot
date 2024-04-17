import os
import streamlit as st
import json  # Import the JSON module
from openai import OpenAI

# Initialize the OpenAI client with the API key
api_key = os.getenv("OPEN_AI_KEY")  # Ensure you have this environment variable set
client = OpenAI(api_key=api_key)

class AIRecruiter:
    def __init__(self, client):
        self.client = client
        self.messages = [
            {"role": "system", "content": """You are Jarvis, the Recruiter is designed to act as a proactive and friendly recruiter."""}
        ]
        self.question_titles = [
            "What do you like to do in your free time? Any particular hobbies or how do you usually spend your weekends?",
            "Where are you living right now?",
            "If you had to name something that truly passions you in life, what would it be?",
            "Could you describe what you do in your current role?",
            "Do you have any personal projects outside of work that you'd like to talk about?",
            "Do you prefer a job with a strict work-life balance, or would you opt for a role that demands more intensity?",
            "What do you consider your standout quality is?",
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

# Streamlit app layout
st.title("Jarvis: The Network's AI Concierge")

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.responses = {}

if st.session_state.question_index < len(recruiter.question_titles):
    question = recruiter.question_titles[st.session_state.question_index]
    user_input = st.text_input("Please answer the question below:", key=str(st.session_state.question_index))
    if st.button("Submit Response"):
        if user_input:  # Ensure non-empty response before proceeding
            st.session_state.responses[question] = user_input
            st.session_state.question_index += 1
            if st.session_state.question_index < len(recruiter.question_titles):
                st.experimental_rerun()
            else:
                st.success("Thank you for your responses!")
                st.write("Here are your responses:")
                for question, answer in st.session_state.responses.items():
                    st.text(f"{question}: {answer}")
                # Saving to a JSON file
                with open('responses.json', 'w') as json_file:
                    json.dump(st.session_state.responses, json_file)
else:
    st.success("You have completed the questionnaire. Here are your responses:")
    for question, answer in st.session_state.responses.items():
        st.text(f"{question}: {answer}")
    # Save responses to JSON when all questions are answered
    with open('responses.json', 'w') as json_file:
        json.dump(st.session_state.responses, json_file)
