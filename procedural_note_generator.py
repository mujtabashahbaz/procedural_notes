import streamlit as st
import openai
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

def extract_info(conversation):
    # Extract Subjective information
    subjective_match = re.search(r'Subjective:(.*?)(?:Objective:|$)', conversation, re.DOTALL | re.IGNORECASE)
    subjective = subjective_match.group(1).strip() if subjective_match else ""
    
    # Extract Objective information
    objective_match = re.search(r'Objective:(.*?)(?:Assessment:|$)', conversation, re.DOTALL | re.IGNORECASE)
    objective = objective_match.group(1).strip() if objective_match else ""
    
    return subjective, objective

def generate_procedural_note(subjective, objective):
    if not openai_installed:
        return "Error: OpenAI library is not installed. Please install it to use this feature."

    api_key = get_openai_api_key()
    if not api_key:
        return "Error: Please enter a valid OpenAI API key to use this feature."

    openai.api_key = api_key

    prompt = f"""Generate a detailed procedural note based on the following patient information:

Subjective: {subjective}

Objective: {objective}

Please provide the following sections:
1. **Diagnosis**:
   - Primary diagnosis
   - At least three differential diagnoses
2. **Procedural Details**:
   - Description of the procedure performed
   - Any intraoperative findings
   - Anesthesia used (if applicable)
3. **Post-Procedure Plan**:
   - Post-operative care instructions
   - Non-pharmacological interventions
   - Pharmacological prescriptions with dosages and frequency
   - Follow-up recommendations
4. **Patient Education**:
   - Important instructions and guidance for recovery and care

Ensure that the note is comprehensive, professional, and formatted using appropriate medical terminology."""

    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app
st.title('AI-Powered Procedural Note Generator')

if not openai_installed:
    st.warning("The OpenAI library is not installed. Some features of this app may not work.")
    st.info("To install the OpenAI library, run the following command in your terminal:")
    st.code("pip install openai")
    st.info("After installing, please restart the Streamlit app.")

# API Key input
api_key = get_openai_api_key()

# ChatGPT conversation input
st.subheader('ChatGPT Conversation')
conversation = st.text_area("Paste your ChatGPT conversation here:", height=200)

# Extract button
if st.button('Extract Subjective and Objective'):
    if conversation:
        subjective, objective = extract_info(conversation)
        st.session_state['subjective'] = subjective
        st.session_state['objective'] = objective
    else:
        st.warning('Please paste a conversation before extracting.')

# Subjective and Objective inputs with explanations
st.subheader('Subjective (Patient-reported Information)')
st.text("This section contains the patient's personal experiences, symptoms, and concerns. \
It includes information provided by the patient about their health, pain levels, history, and any other \
subjective details that may not be observable by the healthcare provider.")
subjective = st.text_area("Subjective information:", value=st.session_state.get('subjective', ''), height=100)

st.subheader('Objective (Clinically Observed Information)')
st.text("This section contains the observable, measurable facts collected during the clinical examination. \
It includes test results, vital signs, physical examination findings, and any other data gathered by the healthcare provider \
during the consultation or procedure.")
objective = st.text_area("Objective information:", value=st.session_state.get('objective', ''), height=100)

# Generate button
if st.button('Generate Enhanced Procedural Note'):
    if subjective and objective:
        if api_key:
            with st.spinner('Generating Enhanced Procedural Note...'):
                procedural_note = generate_procedural_note(subjective, objective)
            st.subheader('Generated Procedural Note')
            st.text_area("", value=procedural_note, height=500)
        else:
            st.warning('Please enter your OpenAI API key to generate the procedural note.')
    else:
        st.warning('Please provide both subjective and objective information.')

# Sidebar Info
st.sidebar.title('About')
st.sidebar.info('This AI-powered app generates detailed procedural notes, including diagnoses, differential diagnoses, treatment plans, and post-operative instructions. Paste a conversation to automatically extract subjective and objective information or input them manually.')

st.sidebar.title('API Key')
st.sidebar.info('This app requires an OpenAI API key to function. Enter it when prompted. The key is not stored permanently and must be re-entered after restarting the app.')

st.sidebar.title('Disclaimer')
st.sidebar.warning('This app is for educational purposes only. The generated notes should not be used for actual medical decision-making without review by a licensed healthcare provider.')
