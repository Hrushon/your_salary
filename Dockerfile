FROM python:3.10-slim

WORKDIR /your_salary

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn","app_run:app","--host", "0.0.0.0","--port", "8000", "--reload"]
