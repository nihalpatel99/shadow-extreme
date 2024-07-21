import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_report(input_prompt,image):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input_prompt, image[0]])
    return response.text


def aircraft_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(aircraft_prompt,question):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([aircraft_prompt,question])
    return response.text

aircraft_prompt = """
You're an expert in technical details in all types of aircraft in terms of exterior and interior. Answer
the prompt and input from the user based on the user input and the answer should be related to aircraft only.
Inputs other than aircraft should be answered as I dont know."
"""

def aircraft_chatbot():
    
    st.header("Aircraft AI Assistant")
    input = st.text_input("Input",key="input")
    submit = st.button("Ask the question")
    if submit:
        response= get_gemini_response(aircraft_prompt,input)
        st.subheader("The response is")
        st.write(response)

st.set_page_config(page_title="ShadowExtreme: Aircraft Exterior Damage Report")



image = Image.open("shadow1.png")
new_image = image.resize((800, 300))
st.image(new_image)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #627277;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("ShadowExtreme: Aircraft Exterior Damage Report Application")

uploaded_file = st.file_uploader("Choose an aircraft image", type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
submit = st.button("Generate Report")

input_prompt = """
You are a Senior Ground Aircraft Enginner responsible for inspecting the aircraft's exterior parts at an airport. Your task is to analyse, inspect, identify and assess the aircraft exterior damage parts
               such as nose, engines, fuselage, wings, tail, landing gear and windows etc.
               and calculate the approximate repair costs neeeded to repair the aircraft. The report should be maximum 600 words. 
               The report format:
               1. Airline
               2. Aircraft type.
               3. Parts that have exterior damage and whether they are minor or major.
               4. Description about the damage.
               5. Approximate Repair costs.
               6. Total Costs.
               7. Status.
               ----
               ----
If the aircraft has no damage or minor damage that does not affect its flight, then the status is green. If the aircraft has
minor damage and does need minor repairs then the status is yellow and the flight may be delayed by few hours.
If the aircraft has major damage and needs major repair then the status is red and the flight needs to be rescheduled, cancelled or
replaced with another stand by aircraft.


"""

if submit:
    image_data = aircraft_image(uploaded_file)
    response = get_report(input_prompt,image_data)
    st.subheader("The response:")
    st.write(response)
    

with st.sidebar:
    st.title("Aircraft Chatbot AI Assistant")
    aircraft_chatbot()
        
            

    
      
                
