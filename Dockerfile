# -----------------------------
# Stage 1: Base Python setup
# -----------------------------
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for efficient Docker caching)
COPY app/requirements.txt ./requirements.txt

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Stage 2: Copy Application Files
# -----------------------------
# Copy the main app folder
COPY app/ ./app

# Copy Streamlit secrets (so Streamlit can find the key)
COPY .streamlit ./app/.streamlit

# -----------------------------
# Stage 3: Environment Config
# -----------------------------
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false \
    PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# -----------------------------
# Stage 4: Run the Streamlit App
# -----------------------------
CMD ["streamlit", "run", "app/travelagent.py", "--server.port=8501", "--server.headless=true"]
