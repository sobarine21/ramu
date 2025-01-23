FROM python:3.11-slim

# Install OpenGL and other necessary dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libx11-dev \
    libfreetype6-dev \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Streamlit app code into the container
COPY . /app

# Expose the Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "streamlit_app.py"]
