# ============================================================
#  Dockerfile — packages the FastAPI app into a container image
# ============================================================

# Start from an official Python image (slim = smaller size)
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer.
# If requirements.txt hasn't changed, pip install is skipped on rebuild.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Tell Docker that the app listens on port 8000
EXPOSE 8000

# Command to run when the container starts
# --host 0.0.0.0 makes the server reachable from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
