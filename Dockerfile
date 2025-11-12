# Use lightweight Python base
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy requirements
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ /app/

# Streamlit config
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONUNBUFFERED=1

EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "travelagent.py", "--server.port=8501", "--server.address=0.0.0.0"]
