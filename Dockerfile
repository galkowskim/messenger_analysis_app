FROM python:3.11

RUN useradd -ms /bin/bash appuser

WORKDIR /app
VOLUME ["/app"]

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appuser /app
RUN chmod -R 755 /app
USER appuser

RUN mkdir -p /home/appuser/.streamlit
COPY src/config.toml /home/appuser/.streamlit/

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

WORKDIR /app/src
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]