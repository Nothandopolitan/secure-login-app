"""Watches network traffic to the app's port and prints basic info.
Needs to run with sudo, since packet capture requires root access.
"""

from scapy.all import sniff, IP, TCP

PORT = 5000


def handle_packet(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        if packet[TCP].dport == PORT or packet[TCP].sport == PORT:
            print(f"{packet[IP].src} -> {packet[IP].dst} "
                  f"(port {packet[TCP].sport} -> {packet[TCP].dport})")


if __name__ == "__main__":
    print(f"Watching traffic on port {PORT}. Press Ctrl+C to stop.")
    sniff(iface="lo", filter=f"tcp port {PORT}", prn=handle_packet, store=False)
