# GPT Bookmarksearching App

## Description

This is an app using Streamlit + Langchain + ChatGPT to search for bookmarks according to user input.

## Installation

To install the application, follow these steps:

1. create a conda environment with `python=3.11` or simply use a environment with `python=3.11`
2. install the requirements with `pip install -r requirements.txt`
3. in `.bashrc`  add the following lines to set system environment variables:
```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
export PINECONE_ENVIRONMENT="gcp-starter"  # gcp-starter for Pinecone free tier
```
## Usage

To use the application, do the following:

1. change the value of `index_name` in `app.py` to your own Pinecone index name 
2. run the app with `streamlit run app.py`
3. click the url that appears in the terminal or it automatically opens in your browser
4. ask for a bookmark  
