FROM public.ecr.aws/lambda/python:3.12

# Install dependencies in two steps for clearer debugging
COPY requirements.txt .

# Upgrade pip and setuptools first (helps with modern packages like langchain/ollama)
RUN pip install --upgrade pip setuptools wheel

# Install your Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src
COPY app.py .

# Lambda handler
CMD ["app.handler"]
