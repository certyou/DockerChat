import socket

# 0.0.0.0 est crucial pour écouter toutes les interfaces dans le container
HOST = '0.0.0.0'  
PORT = 65432

print("--- Le serveur écoute ---")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # Le serveur tourne en boucle pour accepter les connexions
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connecté par {addr}")
            data = conn.recv(1024)
            if data:
                print(f"Message reçu : {data.decode('utf-8')}")
                conn.sendall(b"hi")