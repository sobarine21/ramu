import streamlit as st
import requests
import os

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

# Dropdown to select output format
output_format = st.selectbox(
    "Select output format",
    ["DXF (.dxf)", "STL (.stl)", "SVG (.svg)", "DWG (.dwg)"]
)

# File name input
file_name = st.text_input("Enter the file name:", "generated_output")

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
                # Assuming response contains CAD data in raw text for a selected format
                cad_data = response_data.get("choices", [{}])[0].get("text", "")

                if cad_data:
                    # Determine file extension based on the selected format
                    if output_format == "DXF (.dxf)":
                        cad_extension = ".dxf"
                        mime_type = "application/dxf"
                    elif output_format == "STL (.stl)":
                        cad_extension = ".stl"
                        mime_type = "application/stl"
                    elif output_format == "SVG (.svg)":
                        cad_extension = ".svg"
                        mime_type = "image/svg+xml"
                    elif output_format == "DWG (.dwg)":
                        cad_extension = ".dwg"
                        mime_type = "application/vnd.dwg"

                    # Save the CAD data to a file with the appropriate extension
                    cad_filename = f"{file_name}{cad_extension}"
                    with open(cad_filename, "w") as file:
                        file.write(cad_data)

                    # Provide download link for the generated CAD file
                    with open(cad_filename, "rb") as file:
                        st.download_button(
                            label=f"Download {output_format} file",
                            data=file,
                            file_name=cad_filename,
                            mime=mime_type
                        )

                else:
                    st.error("No CAD data returned from the API.")
            else:
                st.error(f"Error: {response_data.get('error', 'Unknown error occurred.')}")
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            st.error(f"An error occurred: {err}")
