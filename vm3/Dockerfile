FROM python:3.9-slim

WORKDIR /app

COPY client.py server.py /app/

# Par défaut, on lance le serveur, mais on pourra surcharger la commande
CMD ["python", "server.py"]