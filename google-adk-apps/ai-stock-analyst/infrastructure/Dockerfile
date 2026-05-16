FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/frontend
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]