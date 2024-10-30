import streamlit as st
import re

# Check if openai is installed
try:
    import openai
    openai_installed = True
except ImportError:
    openai_installed = False

# Function to get or set the API key
def get_openai_api_key():
    if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
        st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API key:", type="password")
    return st.session_state['openai_api_key']

def generate_procedural_note(patient_info, procedure_details):
    if not openai_installed:
        return "Error: OpenAI library is not installed. Please install it to use this feature."

    api_key = get_openai_api_key()
    if not api_key:
        return "Error: Please enter a valid OpenAI API key to use this feature."

    openai.api_key = api_key
    prompt = f"""Generate a comprehensive procedural note based on the following information:

Patient Information: {patient_info}

Procedure Details: {procedure_details}

Please provide the following sections:
1. Procedure performed:
   - Type of procedure
   - Indication for the procedure
   - Technique used
2. Intraoperative details:
   - Anesthesia type (if applicable)
   - Instruments used
   - Steps taken during the procedure
   - Complications (if any)
3. Post-procedure plan:
   - Immediate post-procedure care
   - Follow-up tests or evaluations
   - Patient education and counseling

Ensure the note is detailed, professional, and follows standard medical terminology and format."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced medical professional generating comprehensive procedural notes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title('AI-Powered Procedural Note Generator for Healthcare Professionals')

if not openai_installed:
    st.warning("The OpenAI library is not installed. Some features of this app may not work.")
    st.info("To install the OpenAI library, run the following command in your terminal:")
    st.code("pip install openai")
    st.info("After installing, please restart the Streamlit app.")

# API Key input
api_key = get_openai_api_key()

# Patient and procedure information input
st.subheader('Patient and Procedure Information')
patient_info = st.text_area("Patient Information (e.g., demographics, medical history, presenting symptoms):", height=100)
procedure_details = st.text_area("Procedure Details (e.g., procedure type, instruments, anesthesia, specific techniques):", height=100)

# Generate button
if st.button('Generate Procedural Note'):
    if patient_info and procedure_details:
        if api_key:
            with st.spinner('Generating Procedural Note...'):
                procedural_note = generate_procedural_note(patient_info, procedure_details)
            st.subheader('Generated Procedural Note')
            st.text_area("", value=procedural_note, height=500)
        else:
            st.warning('Please enter your OpenAI API key to generate the procedural note.')
    else:
        st.warning('Please provide both patient information and procedure details.')

# Add information about the app
st.sidebar.title('About')
st.sidebar.info('This app uses AI to generate comprehensive procedural notes for healthcare professionals. Provide brief patient and procedure details to get a structured, detailed note.')

# Add a note about the API key
st.sidebar.title('API Key')
st.sidebar.info('This app requires an OpenAI API key to function. You\'ll be prompted to enter it when you start the app. Your API key is not stored permanently and will need to be re-entered each time you restart the app.')

# Add a disclaimer
st.sidebar.title('Disclaimer')
st.sidebar.warning('This app is for educational and demonstration purposes only. The generated procedural notes should not be used for actual medical decision-making without review and approval by a licensed healthcare professional.')
