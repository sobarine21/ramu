import streamlit as st
import requests

# Retrieve the token from Streamlit's secrets
token = st.secrets["api"]["FRIENDLI_TOKEN"]

# API details
url = "https://api.friendli.ai/dedicated/v1/completions"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# User input for the text prompt
st.title("Text-to-CAD Generator")
prompt = st.text_area("Enter your prompt:", placeholder="Describe the CAD design or output you need...")
max_tokens = st.slider("Max Tokens", min_value=10, max_value=1511, value=150)
top_p = st.slider("Top P (Controls diversity of responses)", min_value=0.1, max_value=1.0, value=0.8)

if st.button("Generate"):
    if not prompt.strip():
        st.error("Please enter a prompt before generating.")
    else:
        # Prepare the payload
        payload = {
            "model": "5ja6tanymxxt",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        # Send the request
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            response_data = response.json()

            if response.status_code == 200:
                # Display the response
                st.subheader("Generated Output")
                st.code(response_data.get("choices", [{}])[0].get("text", "No response text found"))
            else:
                st.error(f"Error: {response_data.get('error', 'Unknown error occurred.')}")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An error occurred: {err}")
