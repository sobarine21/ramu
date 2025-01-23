# Use a base Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libx11-dev \
    libfreetype6-dev \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]
