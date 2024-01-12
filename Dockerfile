# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Run the initialization script during the image build
RUN python init_db.py

# Expose the port on which the application will run
#EXPOSE 3111

# Command to run your application
CMD ["python", "app.py", "0.0.0.0:3111"]
#CMD ["gunicorn", "--bind", "0.0.0.0:3111", "app:app"]
