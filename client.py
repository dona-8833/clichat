import socket
import threading

HOST = "10.2.255.72"
PORT = 5000


def receive_messages(client_socket):
    """Continuously receive messages from the server."""

    try:
        reader = client_socket.makefile("r", encoding="utf-8")

        for message in reader:
            print(message, end="", flush=True)

        print("\nDisconnected from the server.")

    except (ConnectionError, OSError) as error:
        print(f"\nConnection error: {error}")


def start_client():
    """Connect to the server and start chatting."""

    username = input("Enter your username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))

        # Send the username to the server.
        client_socket.sendall(
            f"{username}\n".encode("utf-8")
        )

        print("Connected to the chat!")
        print("Type your messages and press Enter.")
        print("Type /quit to leave.\n")

        # Start a separate thread to receive messages.
        receiver = threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        )

        receiver.start()

        # The main thread handles user input.
        while True:
            message = input()

            client_socket.sendall(
                f"{message}\n".encode("utf-8")
            )

            if message == "/quit":
                break

    except ConnectionRefusedError:
        print("Could not connect. Is the server running?")

    except (ConnectionError, OSError) as error:
        print(f"Connection error: {error}")

    except KeyboardInterrupt:
        print("\nLeaving the chat...")

    finally:
        client_socket.close()
        print("Client closed.")


if __name__ == "__main__":
    start_client()