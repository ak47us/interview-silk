FROM python:3.10
COPY . .
RUN pip install -r "./src/requirements.txt"
CMD ["python", "./src/main.py"]