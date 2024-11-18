FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app/banking_core:$PYTHONPATH

CMD ["python", "banking_core/main.py"]
