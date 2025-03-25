FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Run the main entrypoint
CMD ["python", "prediction_backend/main.py"]
