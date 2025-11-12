# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ /app/

# Streamlit specific environment
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "travelagent.py", "--server.port=8501", "--server.address=0.0.0.0"]
