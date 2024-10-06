import socket
import threading
from queue import Queue

# Define a thread-safe Queue
queue = Queue()

# A list to store open ports
open_ports = []

# Function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout for connection
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is OPEN")
            open_ports.append(port)
        sock.close()
    except:
        pass

# Worker function for threads
def worker(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

# Main function to initiate scan
def start_scan(ip, port_range):
    print(f"Scanning {ip} for open ports...")

    # Populate the queue with ports to scan
    for port in range(*port_range):
        queue.put(port)
    
    # Create and start threads
    thread_count = 100  # Adjust thread count based on performance needs
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(ip,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    queue.join()

    # Print result
    print(f"\nOpen ports on {ip}: {open_ports if open_ports else 'None'}")

# Example usage
if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    port_range = (1, 1024)  # Scanning ports from 1 to 1024 (common ports)
    
    start_scan(target_ip, port_range)
