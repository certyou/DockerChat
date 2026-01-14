import socket
import threading
import os

# Configuration via variables d'environnement
# Si non défini, on utilise localhost par défaut
SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))

def receive_messages(client_socket):
    # ... (code identique à l'original) ...
    while True:
        try:
            message = client_socket.recv(1024)
            if not message: break
            print(message.decode())
        except: break

import time  # N'oubliez pas d'importer time en haut du fichier
# ... (imports existants)

def start_client():
    """Tente de se connecter au serveur avec des réessais."""
    print(f"Tentative de connexion à {SERVER_HOST}:{SERVER_PORT}...")
    
    client = None
    while True:
        try:
            # On recrée le socket à chaque tentative
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connecté au serveur à {SERVER_HOST}:{SERVER_PORT}")
            break  # Connexion réussie, on sort de la boucle
        except Exception as e:
            print(f"Echec de connexion ({e}). Nouvelle tentative dans 2 secondes...")
            time.sleep(2)

    # Start a thread to listen for messages from the server
    threading.Thread(target=receive_messages, args=(client,)).start()

    # Continuously send messages to the server
    while True:
        try:
            message = input("")  
            if message.lower() == 'exit':
                break
            client.send(message.encode())
        except (EOFError, KeyboardInterrupt):
            break
        except OSError:
            break

    client.close()

if __name__ == "__main__":
    start_client()