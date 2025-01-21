import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

import pandas as pd
import io

st.set_page_config(page_title="🦜🔗 Task breaker")
st.title('🦜🔗 Break down complex tasks')

# hard coding for now. remove before committing
# key = st.sidebar.text_input('OpenAI API Key')

@st.cache_data
def generate_response(topic):
  # Instantiate LLM model
  llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=st.secrets['openai_api_key'])

  # Prompt
  template = """You are experienced project manager (software engineering, house construction, industrial management and agriculture). 
  Use you experience and expertise to break down the following complex task into simple actionable items. Each subtask should be short 
  and direct with an estimated time to complete in minutes, link to an online guide to complete this task, estimated cost of purchases if any. 
  Organize all subtasks into a CSV (separator='|') table with 4 columns: Subtask, Estimated Time (mins), Instructions URL, Purchase URL, Purchase costs (if any) and output the table only. 
  Be brief and do not respond with any other text or code block syntax. The task is '{topic}'."""
  prompt = PromptTemplate(input_variables=["topic"], template=template)
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
