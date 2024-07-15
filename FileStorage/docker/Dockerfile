# Use the official Python image from the Docker Hub
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app/requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY ./app ./app

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]