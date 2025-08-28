# Step 1: Use a base image with Python 3.11
FROM python:3.11-slim as base

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code into the container
COPY . .

# Step 6: Expose port 8000 for FastAPI to run on
EXPOSE 8000

# Step 7: Set the entry point to run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
