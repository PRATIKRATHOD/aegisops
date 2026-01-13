# 1️⃣ Base Python image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copy full source
COPY . .

# 5️⃣ Run pipeline
CMD ["python", "agent_pipeline.py"]
