# Use the official Python image as the build image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the entire application

COPY requirements.txt /app
COPY func /app/func

COPY model_training /app/model_training

COPY saved_model /app/saved_model
COPY vectorizer /app/vectorizer


COPY main.py /app

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install fastapi uvicorn


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]