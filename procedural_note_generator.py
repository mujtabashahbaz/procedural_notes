import streamlit as st
from openai import OpenAI
import re

try:
  import openai
  openai_installed = True
except ImportError:
  openai_installed = False

def get_openai_api_key():
  if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
    st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API key:", type="password")
  return st.session_state['openai_api_key']

def extract_info(conversation):
  # extract subjective and objective

  return subjective, objective

def generate_procedural_note(subjective, objective):

  api_key = get_openai_api_key()

  client = OpenAI(api_key=api_key)

  prompt = f"""
  Generate procedural note using:
  Subjective: {subjective}
  Objective: {objective}
  """

  try:
    response = client.chat.completions.create(
      prompt=prompt,
      model="gpt-3.5-turbo",   
      max_tokens=1500,
      temperature=0.7
    )
    return response['choices'][0]['text'].strip()
  except Exception as e:
    return f"Error: {str(e)}"

# rest of streamlit app 

if __name__ == '__main__':

  # app code

  if st.button('Generate Note'):

    if subjective and objective:

      procedural_note = generate_procedural_note(subjective, objective)

      st.text_area("", value=procedural_note, height=500)