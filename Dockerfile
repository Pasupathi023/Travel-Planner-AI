# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ .

# Streamlit must use port 8080 (Amplify expects this)
EXPOSE 8080

# Run Streamlit
CMD ["streamlit", "run", "travelagent.py", "--server.port=8080", "--server.address=0.0.0.0"]
