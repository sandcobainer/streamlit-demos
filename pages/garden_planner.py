import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import pandas as pd
import io

st.set_page_config(page_title="🦜🔗 Task breaker")
st.title('🦜🔗 Break down complex tasks')

# hard coding for now. remove before committing
# key = st.sidebar.text_input('OpenAI API Key')
key = st.secrets['openai_api_key']

@st.cache_data
def generate_response(topic):
  # Instantiate LLM model
  llm = ChatOpenAI(model_name = "gpt-4o-mini", openai_api_key = key)

  # Prompt
  template = """You are """
  prompt = PromptTemplate(input_variables = ["topic"], template = template)
  prompt_query = prompt.format(topic=topic)

  # Run LLM model
  response = llm.invoke(prompt_query) 
  print('Got repsonse from openai', response.content)
  return response

def parse_response(response):
  text = response.content
  df = pd.read_csv(io.StringIO(text), sep='|')
  # df.loc['Total', :] = df.sum(numeric_only=True)
  df["Completion"] = False

  st.data_editor(
    df,
    column_config = {
      "Completion Status" : st.column_config.CheckboxColumn(
        help = "Click to mark as completed", 
        default = False
      ),

      "Instructions URL":st.column_config.LinkColumn(
        help = "Link to an instructional video, website to help you with this task"
      ),
      "Purchase URL":st.column_config.LinkColumn(
        help = "Link to a website where materials can be purchased for this task"
      )
    }
  )
  return 

with st.form('my_form'):
  text = st.text_area('Enter a task to breakdown:', 'how to build a solar battery system?')
  submitted = st.form_submit_button('Submit')
  # if not key.startswith('sk-'):
  #   st.warning('Please enter your OpenAI API key!', icon='⚠')
  # if submitted and key.startswith('sk-'):
  response = generate_response(text)
  parse_response(response)
