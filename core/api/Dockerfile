FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn==0.27.0 \
    neo4j==5.15.0 \
    pydantic==2.5.3 \
    psycopg2-binary==2.9.9

# Copy API code
COPY main.py .

# Skills will be mounted as volume
# /app/skills

# Expose API port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
