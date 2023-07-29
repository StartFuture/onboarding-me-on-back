FROM python:3.10

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 


CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"] 