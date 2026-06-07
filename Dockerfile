FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (build-essential for compiling C-extensions, curl, git)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
# Hugging Face Spaces expose port 7860 by default

# Expose Streamlit port
EXPOSE 7860

# Give execution permission to the startup script
RUN chmod +x start.sh

# Start both FastAPI and Streamlit using the script
CMD ["./start.sh"]
