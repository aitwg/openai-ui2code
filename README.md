# OpenAI UI to Code Streamlit App

Inspired by Gemini UI to Code, porting to OpenAI API to support other OpenAI compatible models.
This Streamlit app is designed to convert UI designs into code using the power of AI. It analyzes uploaded images of UI designs and generates corresponding HTML code, making it easier for developers to bring their designs to life.

## Installation

To install the necessary dependencies, run the following command:

```
pip install -r requirements.txt
```

## Configuration

https://ai.google.dev/gemini-api/docs/openai

edit gemini.sh

'''
export GEMINI_API_KEY='YOU API KEY'
export OPENAI_MODEL_NAME=gemini-1.5-flash
export OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
'''

## Running the App

To run the app, use the following command:

test gemini 1.5 model
```
./gemini.sh
streamlit run app.py
```

test openai/gpt4o thru routerai
```
./gpt4o.sh
streamlit run app.py
```

## Misc

Before running the app, you need to configure your API key. 
Replace `YOUR API KEY` with your actual API key to enable the AI functionalities.

You can also change the  model you want and even tell it to use a specific CSS framework.