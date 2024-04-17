from openai import OpenAI
import os
import streamlit as st

api_key = os.environ.get("OPEN_AI_KEY")  # Replace with your actual API key
client = OpenAI(api_key=api_key)

class AIRecruiter:
    def __init__(self, client):
        self.client = client
        self.messages = [
            {"role": "system", "content": """You are Jarvis, the Recruiter is designed to act as a proactive and friendly recruiter.
            Jarvis listens actively to responses, providing related follow-ups to ensure the candidate feels heard but Jarvis must give short related follow-up responses, 
            and do not try to always relate his responeses to job related subjects. 
            It should ensure candidate feels heard but trying to give a more natural response as short as possible.
            It emphasizes that the information collected is for curating high-quality personalized recomendations, with a guarantee of privacy and non-spammy communication. 
            Jarvis avoids being pushy and respects candidates' preferences on sharing details. 
            It leads the conversation and does not reask for clarity, accepting the first response provided by the user. 
            The tone is balanced, neutral, and helpful, maintaining professional decorum without being overly formal or too casual. 
            Jarvis follow the instructions precisely. It does not change the questions provided."""}
        ]
        self.question_titles = [
            "What do you like to do in your free time? Any particular hobbies or how do you usually spend your weekends?",
            "Where are you living right now?",
            "If you had to name something that truly passions you in life, what would it be? Do you have a passion that stands out from your everyday hobbies?",
            "Could you describe what you do in your current role? What technologies or frameworks do you work with daily?",
            "Do you have any personal projects outside of work that you'd like to talk about?",
            "Do you prefer a job with a strict work-life balance, or would you opt for a role that demands more intensity and possibly longer hours?",
            "What do you consider your standout quality is, or what aspect of your work that really defines you?",
            "Do you have any short-term or long-term professional goals?",
            "Do you feel confident in your English skills to engage in daily fluent conversations?",
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
            st.success(response)

    if st.button('Next Question', key=f"next_{st.session_state.question_index}"):
        st.session_state.question_index += 1  # Increment to move to the next question

# End of all questions
if st.session_state.question_index >= len(recruiter.question_titles):
    st.success("Thank you for your responses!")
    st.write("Here are your responses:")
    for q, a in st.session_state.responses.items():
        st.write(f"{q}: {a}")

