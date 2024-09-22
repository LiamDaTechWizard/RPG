import socket
import threading
import random

class Entity:
    def __init__(self, name):
        self.name = name

    def action(self):
        roll = random.randint(1, 20)
        if roll >= 15:
            return f"{self.name} attacks with great strength!"
        elif roll >= 10:
            return f"{self.name} makes a standard attack."
        else:
            return f"{self.name} misses the attack."

class GameServer:
    def __init__(self):
        self.entities = [Entity("Goblin"), Entity("Orc"), Entity("Troll")]
        self.players = []

    def handle_client(self, client_socket):
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            self.broadcast(message)
        client_socket.close()

    def broadcast(self, message):
        for player in self.players:
            player.send(message.encode())

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 5555))
        server.listen()
        print("Server started, waiting for players...")

        while True:
            client_socket, addr = server.accept()
            print(f"Player {addr} connected.")
            self.players.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    GameServer().start()
