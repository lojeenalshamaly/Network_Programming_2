import socket
import threading

# Bank account details
accounts = {
    '1111': 100000,
    '2222': 200000,
    '3333': 300000,
    '4444': 400000
}


def handle_client(client_socket):
    account_number = client_socket.recv(1024).decode()
    if account_number in accounts:
        client_socket.send(b"Welcome! You have connected to the bank server.")
    else:
        client_socket.send(b"Invalid account number. Connection terminated.")
        client_socket.close()
        return

    while True:
        option = client_socket.recv(1024).decode()

        if option == '1':
            balance = accounts[account_number]
            client_socket.send(f"Your current balance is: {balance}".encode())
        elif option == '2':
            amount = int(client_socket.recv(1024).decode())
            accounts[account_number] += amount
            client_socket.send(f"Deposit successful. Your new balance is: {accounts[account_number]}".encode())
        elif option == '3':
            amount = int(client_socket.recv(1024).decode())
            if accounts[account_number] >= amount:
                accounts[account_number] -= amount
                client_socket.send(f"Withdrawal successful. Your new balance is: {accounts[account_number]}".encode())
            else:
                client_socket.send("Insufficient funds. Withdrawal failed.".encode())
        else:
            break

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 12345))
    server.listen(5)
    print("Server listening on port 12345...")

    while True:
        client_socket, address = server.accept()
        print(f"Connection from {address} established.")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


start_server()
