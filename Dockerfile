FROM python:3.10

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
