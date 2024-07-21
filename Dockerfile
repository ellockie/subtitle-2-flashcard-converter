# Use Python 3.12 with Alpine
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install build dependencies, install Python packages, then remove build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copy the rest of your application's code (diabled, to prevent image rebuilding on each edit)
#COPY . .

# Command to run your application
CMD ["python", "main.py"]
