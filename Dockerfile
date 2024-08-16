FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

# Run app.py when the container launches
CMD ["fastapi", "dev", "main.py"]
