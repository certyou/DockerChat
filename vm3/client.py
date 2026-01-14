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

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connecté au serveur {SERVER_HOST}:{SERVER_PORT}")
    except Exception as e:
        print(f"Impossible de se connecter au serveur : {e}")
        return

    threading.Thread(target=receive_messages, args=(client,)).start()

    while True:
        try:
            message = input("")
            if message.lower() == 'exit': break
            client.send(message.encode())
        except EOFError: # Gestion de l'erreur si le container n'a pas de TTY interactif
            break
            
    client.close()

if __name__ == "__main__":
    start_client()