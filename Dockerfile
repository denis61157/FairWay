# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /FairWay

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY . .

# Expose the necessary port for the bot
EXPOSE 9000

# Run the bot when the container launches
CMD ["python", "bot.py"]
