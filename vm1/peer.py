import socket
import threading
import os
import sys
import time

# --- CONFIGURATION ---
# Mon port d'écoute (celui que j'ouvre aux autres)
MY_PORT = int(os.getenv('MY_PORT', 5000))

# L'adresse du Pair (l'autre machine)
PEER_IP = os.getenv('PEER_IP', '127.0.0.1')
PEER_PORT = int(os.getenv('PEER_PORT', 5000))

def start_listening():
    """Agit comme un SERVEUR : écoute les messages entrants."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 0.0.0.0 est CRUCIAL pour Docker
    server.bind(('0.0.0.0', MY_PORT))
    server.listen(5)
    print(f"[*] Écoute sur le port {MY_PORT}...")

    while True:
        try:
            client_socket, addr = server.accept()
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n[Reçu du Pair] : {message}")
                # Réaffiche le prompt pour l'utilisateur
                print("Moi > ", end='', flush=True)
            client_socket.close()
        except Exception as e:
            print(f"Erreur d'écoute: {e}")

def start_sending():
    """Agit comme un CLIENT : envoie les messages."""
    print(f"[*] Prêt à envoyer vers {PEER_IP}:{PEER_PORT}")
    
    while True:
        try:
            msg = input("Moi > ")
            if not msg: continue
            
            # Connexion éphémère : On ouvre, on envoie, on ferme
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Timeout court pour ne pas bloquer si l'autre est éteint
            s.settimeout(5) 
            try:
                s.connect((PEER_IP, PEER_PORT))
                s.send(msg.encode())
                s.close()
            except Exception as e:
                print(f"Erreur: Impossible de joindre {PEER_IP}:{PEER_PORT} ({e})")
                
        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    print("--- CHAT P2P ---")
    
    # Lancer l'écoute dans un thread séparé
    listen_thread = threading.Thread(target=start_listening)
    listen_thread.daemon = True # Le thread mourra quand le programme principal quittera
    listen_thread.start()

    # Lancer l'envoi dans le thread principal
    start_sending()