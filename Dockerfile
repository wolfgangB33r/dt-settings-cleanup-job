# Use the official Python lightweight image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into /app
COPY . /app
# Use a small Python image
FROM python:3.12-slim

# Copy your app
COPY app.py /app/app.py
WORKDIR /app

# Expose port (for local clarity — Cloud Run sets this automatically)
EXPOSE 8080

# Run the server
CMD ["python", "app.py"]
