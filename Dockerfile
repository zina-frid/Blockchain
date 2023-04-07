FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENTRYPOINT ["python","blockchain/src/main.py"]
