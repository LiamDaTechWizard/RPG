import socket
import tkinter as tk
from threading import Thread

class GameClient:
    def __init__(self, master):
        self.master = master
        self.master.title("RPG Game")
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.map_label = tk.Label(self.frame, text="Map: (https://as1.ftcdn.net/v2/jpg/05/64/98/88/1000_F_564988843_870IwWPnyoGXdMFZNaOfLyJSzM0sxnrB.jpg)", font=("Arial", 16))
        self.map_label.pack()

        self.text_area = tk.Text(self.frame, height=10, width=50)
        self.text_area.pack()

        self.action_entry = tk.Entry(self.frame)
        self.action_entry.pack()
        self.action_entry.bind("<Return>", self.send_action)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 5555))

        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_action(self, event):
        action = self.action_entry.get()
        self.socket.send(action.encode())
        self.action_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                self.text_area.insert(tk.END, message + "\n")
                self.text_area.see(tk.END)
            except:
                print("An error occurred!")
                self.socket.close()
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = GameClient(root)
    root.mainloop()
