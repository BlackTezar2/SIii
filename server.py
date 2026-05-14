import socket
import sys

# Listening on port 443
HOST = '0.0.0.0'
PORT = 443

print(f"Server is listening on port {PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    
    conn, addr = s.accept()
    with conn:
        print(f"Connection established from {addr}.")
        
        # Receive data
        data = conn.recv(4096)
        if data:
            print(f"Received: {len(data)} bytes")
            print(f"First bytes: {data[:50].hex()}")
            
            # Check handshake type
            # First byte protocol type (0x16 = Handshake)
            # Fifth byte handshake type (0x01 = Client Hello)
            if len(data) > 5:
                proto = data[0]
                handshake_type = data[5]
                
                if proto == 0x16 and handshake_type == 0x01:
                    print("✅ This is a Client Hello!")
                    print("Simulation completed successfully.")
                else:
                    print("❌ This is not a standard Client Hello.")
            else:
                print("Received data is too short.")
                
            # Send a simple response (optional - for testing)
            # If you want to complete the full cycle, you could build a Server Hello
            # But for testing reception, this is sufficient.
            conn.send(b"\x16\x03\x03\x00\x01\x01") # A small response
            print("Small response sent.")