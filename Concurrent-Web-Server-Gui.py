import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import sys

SERVER_HOST = '0.0.0.0'  # Bind to all interfaces
BUFFER_SIZE = 1024

# Function to handle client requests concurrently
def handle_client(client_socket, log_text):
    try:
        # Receive data from the client
        request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        log_text.insert(tk.END, f"Received: {request}\n")
        log_text.yview(tk.END)
        
        # Send a response back to the client
        response = f"Server Response: {request} - Successfully received!"
        client_socket.send(response.encode('utf-8'))
        
        log_text.insert(tk.END, f"Sent: {response}\n")
        log_text.yview(tk.END)
    except Exception as e:
        log_text.insert(tk.END, f"Error handling client: {e}\n")
        log_text.yview(tk.END)
    finally:
        client_socket.close()

# Function to create and start the server
def start_server(host, port, log_text):
    try:
        # Create the socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Allow up to 5 connections in the backlog
        
        log_text.insert(tk.END, f"Server listening on {host}:{port}...\n")
        log_text.yview(tk.END)
        
        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            log_text.insert(tk.END, f"Connection from {client_address} established.\n")
            log_text.yview(tk.END)
            
            # Handle the client request in a separate thread
            client_handler = threading.Thread(target=handle_client, args=(client_socket, log_text))
            client_handler.start()
    
    except Exception as e:
        log_text.insert(tk.END, f"Error starting server: {e}\n")
        log_text.yview(tk.END)
        sys.exit(1)

# Function to trigger server start from the GUI
def on_start_button_click(log_text):
    host = host_entry.get() or '0.0.0.0'
    try:
        port = int(port_entry.get())
        start_server(host, port, log_text)
    except ValueError:
        log_text.insert(tk.END, "Invalid port number. Please enter a valid port.\n")
        log_text.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Concurrent Web Server")
root.geometry("600x400")

# Add a label and entry for the host (IP address)
host_label = tk.Label(root, text="Server Host (IP Address):")
host_label.pack(pady=5)
host_entry = tk.Entry(root, width=30)
host_entry.pack(pady=5)
host_entry.insert(0, '0.0.0.0')  # Default value

# Add a label and entry for the port
port_label = tk.Label(root, text="Server Port:")
port_label.pack(pady=5)
port_entry = tk.Entry(root, width=30)
port_entry.pack(pady=5)
port_entry.insert(0, '8080')  # Default port

# Add a button to start the server
start_button = tk.Button(root, text="Start Server", command=lambda: on_start_button_click(log_text))
start_button.pack(pady=10)

# Add a scrolled text box to display server logs
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, state=tk.DISABLED)
log_text.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
