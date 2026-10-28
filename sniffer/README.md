## What it does

watch_traffic.py uses Scapy to watch raw network packets going to and from port 5000 (where the app runs). It needs sudo, since capturing packets requires root access.

## Known limitation

It had to be pointed at the loopback interface (lo) specifically, since app traffic on 127.0.0.1 doesn't always appear on Scapy's default interface. Fixed by passing iface="lo" to sniff().

It shows that traffic is happening and which ports are involved, but doesn't decode the actual HTTP content (username/password) — that would need deeper packet inspection, which is beyond this basic version.