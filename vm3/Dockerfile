FROM python:3.9-slim

WORKDIR /app

# Cette ligne force Python à afficher les logs instantanément
ENV PYTHONUNBUFFERED=1

COPY client.py server.py /app/

CMD ["python", "server.py"]