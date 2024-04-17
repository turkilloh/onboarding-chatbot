from openai import OpenAI
import os
import streamlit as st

api_key = os.environ.get("OPEN_AI_KEY")  # Replace with your actual API key
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
            "Do you feel confident in your English skills?",
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

recruiter = AIRecruiter(client)

# Streamlit application setup
st.title("Jarvis: The Network's AI Concierge")

# Initialize session state for handling the index and responses
if 'initiated' not in st.session_state:
    st.session_state.initiated = False
    st.session_state.question_index = 0
    st.session_state.responses = {}

# Display the initial greeting and wait for user to start
if not st.session_state.initiated:
    st.write("Hey, I'm Jarvis, The Network's AI Concierge. Should we get started with the onboarding?")
    if st.button("Yes, let's start"):
        st.session_state.initiated = True
    elif st.button("No, thank you"):
        st.stop()

# Handle the detailed questions and responses
if st.session_state.initiated and st.session_state.question_index < len(recruiter.question_titles):
    question = recruiter.question_titles[st.session_state.question_index]
    user_input = st.text_input(f"{question}", key=f"user_input_{st.session_state.question_index}")

    if st.button('Submit Answer', key=f"submit_{st.session_state.question_index}"):
        if user_input:  # Check for user input before proceeding
            response = recruiter.send_message(user_input)
            st.session_state.responses[question] = user_input
            st.session_state['response_submitted'] = True
            st.success(response)

    if st.button('Next Question', key=f"next_{st.session_state.question_index}") or 'response_submitted' in st.session_state:
        st.session_state.question_index += 1  # Increment to move to the next question
        st.session_state.pop('response_submitted', None)  # Clear the flag after moving to the next question

# End of all questions
if st.session_state.question_index >= len(recruiter.question_titles):
    st.success("Thank you for your responses!")
    st.write("Here are your responses:")
    for q, a in st.session_state.responses.items():
        st.write(f"{q}: {a}")
