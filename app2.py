from openai import OpenAI
import os
import streamlit as st

api_key = os.environ.get("OPEN_AI_KEY")  # Replace with your actual API key
client = OpenAI(api_key=api_key)

import re

class AIRecruiter:
    def __init__(self, client):
        self.client = client
        self.messages = [{
            "role": "system",
            "content": """You are Jarvis, the Recruiter is designed to act as a proactive and friendly recruiter.
            You should start by saying, 'Hey, I'm Jarvis, The Network's AI Concierge. Should we get started with the onboarding?'
            Upon receiving a 'yes' reply, you will precisely ask the candidate a series of detailed questions in the following order:
            1. What do you like to do in your free time? Any particular hobbies or how do you usually spend your weekends?
            2. Where are you living right now?
            3. If you had to name something that truly passions you in life, what would it be? Do you have a passion that stands out from your everyday hobbies?
            4. Could you describe what you do in your current role? What technologies or frameworks do you work with daily? Has there been any project in your career that you found particularly exciting? Since we have your LinkedIn profile, I see you're currently working as [X] at [Y]. Could you share more about your responsibilities there?
            5. Do you have any personal projects outside of work that you'd like to talk about?
            6. Do you prefer a job with a strict work-life balance, such as working from 9 to 6, or would you opt for a role that demands more intensity and possibly longer hours?
            7. What do you consider your standout quality is, or what aspect of your work that really defines you?
            8. Do you have any short-term or long-term professional goals?
            9. Do you feel confident in your English skills to engage in daily fluent conversations?
            10. What is your current salary, and what would be a tempting offer for you to consider switching jobs?
            11. Is there anything specific you'd like to share that could help us present you with better opportunities?
            Jarvis listens actively to responses, providing related follow-ups to ensure the candidate feels heard. 
            Jarvis must not give long related follow-up responses, it should ensure candidate feels heard but trying to give a more natural response.
            It emphasizes that the information collected is for curating high-quality, personalized job opportunities, with a guarantee of privacy and non-spammy communication. 
            Jarvis avoids being pushy and respects candidates' preferences on sharing details. 
            It leads the conversation and does not reask for clarity, accepting the first response provided by the user. 
            The tone is balanced, neutral, and helpful, maintaining professional decorum without being overly formal or too casual. 
            Jarvis follow the instructions precisely. It does not change the questions provided."""
        }]
        detailed_content = self.messages[0]['content']
        self.question_titles = self.extract_questions(detailed_content)
        self.responses = {}
        self.question_index = 0

    def extract_questions(self, content):
        # Extract the numbered questions using regex
        questions = re.findall(r'\d+\.\s(.*?)(?=\d+\.\s|$)', content)
        return questions

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
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.responses = {}

# Interaction logic
if st.session_state.question_index < len(recruiter.question_titles):
    # Display the question based on the current index
    question = recruiter.question_titles[st.session_state.question_index]
    user_input = st.text_input(f"{question}: ", key=f"user_input_{st.session_state.question_index}")
    
    # Button to submit response and move to next question
    if st.button('Next', key=f"next_{st.session_state.question_index}"):
        if user_input:  # Ensure there is input before processing
            response = recruiter.send_message(user_input)
            # Store the response corresponding to the current question
            st.session_state.responses[question] = user_input
            st.session_state.question_index += 1
            
            # Display the AI's response if not the end of the conversation
            if st.session_state.question_index < len(recruiter.question_titles):
                st.success(response)
            else:
                st.success("Thank you for your responses!")
                # Optionally print all responses after the conversation ends
                st.write("Here are your responses:")
                for question, answer in st.session_state.responses.items():
                    st.write(f"{question}: {answer}")
        else:
            st.error("Please enter a response to proceed.")


# After all questions have been asked, the responses dictionary is complete
print("Here are your responses:")
#print(recruiter.responses.items())
for question, answer in recruiter.responses.items():
   print(f"{question}: {answer}")

    

