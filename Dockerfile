

# Use the official Python image as the build image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory
WORKDIR ${LAMBDA_TASK_ROOT} 

# Copy the entire application
COPY requirements.txt ${LAMBDA_TASK_ROOT} 
COPY main.py ${LAMBDA_TASK_ROOT} 
COPY saved_model ${LAMBDA_TASK_ROOT}/saved_model
COPY vectorizer ${LAMBDA_TASK_ROOT}/vectorizer
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt  
RUN pip install fastapi uvicorn

CMD ["main.process_text"]