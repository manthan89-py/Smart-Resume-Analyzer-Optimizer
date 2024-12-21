# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Make port 7860 available to the world outside this container
# (7860 is the default Gradio port)
EXPOSE 7860

# Run app.py when the container launches
CMD ["python", "app.py"]