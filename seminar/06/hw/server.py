#!/bin/python3
import socket
import threading

# Connection parameters
host = '172.16.1.11'
port = 55555

# Configuring and starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for clients and their nicknames
clients = []
nicknames = []


# Sending messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling messages from clients
def handle(client):
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf8'))
            nicknames.remove(nickname)
            break


# Receiving / listening function
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print('Connected with {}'.format(str(address)))

        # Request and store nickname
        client.send('NICK'.encode('utf8'))
        nickname = client.recv(1024).decode('utf8')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print('Nickname is {}'.format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf8'))
        client.send('Connected to server!'.encode('utf8'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Chat server started...')
receive()
