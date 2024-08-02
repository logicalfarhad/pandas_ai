import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from os.path import dirname, join
from pandasai import SmartDataframe
from llms.CustomMistralLLM import CustomMistralLLM
import os

# Load environment variables
load_dotenv()


st.set_page_config(page_title='Data Analysis with Pandas AI')
st.title('Data Analysis with Pandas AI')


uploaded_file = st.file_uploader("Choose a .csv file", type="csv")


LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
#llm = Ollama(model="mistral", base_url=LLM_ENDPOINT)
api_url = LLM_ENDPOINT
api_token = os.getenv("LLM_AUTH_TOKEN")

llm = CustomMistralLLM(
    api_url,
    api_token
)

# Check if a file has been uploaded
if uploaded_file:
    # Read the uploaded CSV file into a pandas dataframe
    data = pd.read_csv(uploaded_file)
    
    st.subheader(f"File uploaded: {uploaded_file.name}")
    st.write(data.head(2))
    
    # Define a path to save charts (if needed)
    base_path = dirname(__file__)
    save_charts_path = join(base_path, 'exports', 'charts')
    print(save_charts_path)
    
    # Initialize SmartDataframe for interactive data analysis
    smart_df = SmartDataframe(data, config= {
        "llm": llm,
        "verbose": True,
        'open_charts': True,
       # 'save_charts': True,   # Save generated charts
       # 'enable_cache': False
    })
    
    prompt = st.text_area("Enter your prompt:")

    # Generate a response when the button is clicked
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                try:
                    # Get the response from the SmartDataframe
                    response = smart_df.chat(prompt)
                    if isinstance(response, pd.DataFrame):
                        st.write(response)
                    elif isinstance(response, str) and response.endswith(".png"):
                        st.image(response)
                    else:
                        st.write(response)
                except Exception as e:
                    # Display an error message if there's an issue
                    st.error(f"Error generating response: {e}")
        else:
            # Warn the user if the prompt is empty
            st.warning("Please enter a prompt!")
