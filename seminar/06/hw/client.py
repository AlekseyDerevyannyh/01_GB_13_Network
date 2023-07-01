import socket
import threading

# Connection parameters
host = '172.16.1.11'
port = 55555

# Enter nickname
nickname = input("Enter your nickname: ")

# Configuring connection and connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 and TCP
client.connect((host, port))  # server IP and port


# Listening to server and sending nickname
def receive():
    while True:
        try:
            # Receive message from server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf8')
            if message == 'NICK':
                client.send(nickname.encode('utf8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print('Error receiving message!')
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        try:
            client.send(message.encode('utf8'))
        except:
            print('Error sending message!')
            client.close()


# Starting threads for listening and writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
