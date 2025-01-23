import streamlit as st
import google.generativeai as genai
import cadquery as cq
from cadquery import exporters
import tempfile
import os
import json

# Configure Gemini AI with API key securely stored in Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to process prompt with Gemini AI
def parse_prompt_with_gemini(prompt):
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Get the response from Gemini
        response = model.generate_content(prompt)
        
        # Parse the JSON-like structure returned by Gemini
        cad_data = json.loads(response.text)  # Ensure the response is valid JSON
        return cad_data
    except Exception as e:
        st.error(f"Error communicating with Gemini AI: {e}")
        return None

# Function to dynamically process CAD instructions
def execute_cad_instructions(instructions):
    try:
        workplane = cq.Workplane("front")  # Start with a default workplane
        
        # Process instructions dynamically
        for step in instructions:
            action = step.get("action")
            params = step.get("params", {})
            
            # Dynamically execute CadQuery methods
            if hasattr(workplane, action):  # Check if the method exists in CadQuery
                workplane = getattr(workplane, action)(**params)
            else:
                st.warning(f"Unsupported action: {action}")
        
        return workplane
    except Exception as e:
        st.error(f"Error generating CAD design: {e}")
        return None

# Function to export the generated CAD object to an STL file
def export_cad_to_file(cad_object):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "dynamic_model.stl")
    exporters.export(cad_object, file_path)
    return file_path

# Streamlit App UI
st.title("Dynamic Text-to-CAD Application")
st.write("Describe your design using natural language. Gemini AI will generate a CAD model dynamically!")

# Prompt input field
prompt = st.text_area(
    "Enter your design prompt:",
    "Design a rectangular box of 5x3x2 cm and move it 10 cm upwards."
)

# Button to process the prompt and generate the CAD model
if st.button("Generate CAD Design"):
    if not prompt.strip():
        st.error("Please enter a valid prompt!")
    else:
        st.info("Processing your request...")
        
        # Step 1: Parse the prompt with Gemini AI
        gemini_response = parse_prompt_with_gemini(prompt)
        if gemini_response:
            st.write("Gemini AI Parsed Response:", gemini_response)
            
            # Step 2: Execute CAD instructions dynamically
            cad_model = execute_cad_instructions(gemini_response.get("steps", []))
            if cad_model:
                st.success("CAD design generated successfully!")
                
                # Step 3: Export the CAD object to STL
                file_path = export_cad_to_file(cad_model)
                
                # Step 4: Provide download button for the STL file
                st.download_button(
                    label="Download CAD File (STL)",
                    data=open(file_path, "rb"),
                    file_name="generated_model.stl",
                    mime="application/octet-stream",
                )
                st.write("Your CAD model is ready for download!")
            else:
                st.error("Failed to generate CAD model!")

