# Dockerfile for Streamlit app
FROM python:3.11-slim

# set working dir
WORKDIR /app

# copy and install python deps
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy app code
COPY . .

# streamlit config + python unbuffered for logs
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false

EXPOSE 8501

# run streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
