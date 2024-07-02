FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

# copy everything in current local dir to docker dir
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

