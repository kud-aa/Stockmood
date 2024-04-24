FROM python:3.8

COPY requirements.txt requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
