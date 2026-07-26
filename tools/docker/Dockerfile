FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the phi-qml package
RUN pip install -e .

# Expose the port for the web application
EXPOSE 8080

# Default command: run the CLI
CMD ["phi", "repl"]
