FROM python:3.10

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

WORKDIR /app

COPY ./app /app/app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# the inner logic saves the active workout connection in RAM, so we need to run only one worker
# since there arises a case when a connection is saved in `A` worker and the request is handled by `B` worker raising errors
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "-w", "1"]
