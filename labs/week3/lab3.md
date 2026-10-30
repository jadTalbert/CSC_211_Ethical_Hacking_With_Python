### Week 3 Lab 3: Assignment: Active Reconnaissance(Direct Network Probing) Continued

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-04,T-06,T-07,T-09,T-10,T-11,T-13,T-14,T-16,T1070,T1341,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-03,S-05,S-06,S-10,S-13,S-17,S-19,S0532,S0543,S0572,S0597,S0688](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-03,K-05,K-08,K-10,K0674,K0680,K0682,K0683,K0797,K0813,K0833,K0882,K0924,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

### Context
The CSO is putting you under a bit more pressure to get things done faster, and after learning how to ping servers using Python in the previous hacking exercise, you're feeling a bit more confident in your White-Hat Hacking abilities. You have learned through past conversations with other colleagures, that port scanning is an important aspect of Ethical Hacking and you move on to scanning TCP Ports on these same docker containers(e.g. the `student-recon` docker container).



### Port Scanner:
You sit down and think about how you want to approach this problem, and decide the most obvious file name for this python program will be `tcp_scanner.py`. However, you don't recall exaclty what TCP stands for nor what it is used for, so you do some research using Google's Gemini AI platform and prompt the AI with this statement: `Explain in layman terms what TCP stands for and what it does.`

After your research is complete, you have a better idea of what you need to accomplish, but you still don't quite understand how to accomplish port scanning using python. Therefore, you need to do more research. 

Using Gemini again for your task, you prompt the AI with the following: `tell me about the python libraries that can help me complete an ethical port scan for my employer`.

Based on your new found knowledge of sockets, you meet with your team and explain what you have learned and ask two colleagues to take your research and build a python program that will allow the team to perform port scans. You also let them know that this has to be time-boxed, as the CSO is interested in getting this done quickly.

After your co-workers complete the program, you realize they used Generative AI to do this for them and there are no comments in the code. In order for others to understand the code in the future, you take the time to understand the logic and properly comment the code.

### tcp_scanner.py File

```python

##################################################################
# You should take the time and comment the code in this #program #
##################################################################

import socket
import sys

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    1194: "OpenVPN",
    3000: "Node / Dev Frontend",
    3306: "MySQL / MariaDB",
    5432: "PostgreSQL",
    8080: "HTTP-Alt / Dev-API",
    27017: "MongoDB"
}

def scan_target(target_ip: str, ports: dict, timeout: float = 0.8):
    print(f"[*] Scanning Target: {target_ip}")
    print(f"{'PORT':<10} {'STATE':<10} {'SERVICE'}")
    print("-" * 35)

    open_ports = []
    for port, service_hint in ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        # connect_ex returns 0 on successful TCP handshake (SYN -> SYN-ACK -> ACK)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"{port:<10} {'OPEN':<10} {service_hint}")
            open_ports.append(port)
        s.close()
        
    print("-" * 35)
    return open_ports

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "172.29.0.2"
    scan_target(target, COMMON_PORTS)
```



### Script 3: Service Banner Grabber (`scripts/03_banner_grabber.py`)

Interrogates an open TCP port by listening for default daemon banners or sending an HTTP probe.

```python
#!/usr/bin/env python3
"""
03_banner_grabber.py: Service fingerprinting and metadata extraction.
"""

import socket
import sys

def grab_raw_banner(ip: str, port: int, timeout: float = 1.5) -> str:
    """Read initial greeting messages sent by daemons like SSH, FTP, or SMTP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner
    except Exception:
        return ""

def grab_http_banner(ip: str, port: int, timeout: float = 1.5) -> str:
    """Send an active HTTP probe to extract Server and runtime headers."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            probe = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: LabScanner/1.0\r\n\r\n"
            s.sendall(probe.encode())
            response = s.recv(2048).decode(errors="ignore")
            
            for line in response.split("\r\n"):
                if line.lower().startswith("server:"):
                    return line
            return response.split("\r\n")[0] if response else ""
    except Exception:
        return ""

def fingerprint_service(ip: str, port: int):
    # Attempt a raw banner read first
    banner = grab_raw_banner(ip, port)
    
    # If the service does not announce itself, send an active HTTP probe
    if not banner:
        banner = grab_http_banner(ip, port)
        
    if banner:
        print(f"[+] {ip}:{port} -> {banner}")
    else:
        print(f"[-] {ip}:{port} -> Port is open, but daemon remained silent.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python 03_banner_grabber.py <IP> <PORT>")
        sys.exit(1)
        
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    fingerprint_service(target_ip, target_port)
```

### Script 4: Automated DNS-to-Port-Scan Pipeline (`scripts/04_recon_pipeline.py`)

Chains DNS record resolution into automated socket sweeps against discovered endpoints.

```python
#!/usr/bin/env python3
"""
04_recon_pipeline.py: End-to-end pipeline bridging DNS recon to active socket scans.
"""

import dns.resolver
import socket

DNS_SERVER = "172.29.0.53"
DOMAIN = "acme-corp.com"
TARGET_HOSTS = ["dev-api", "stage", "corp-db", "vpn", "mail", "www", "ns1"]
PORTS_TO_AUDIT = [21, 22, 25, 53, 80, 443, 1194, 3000, 3306, 8080]

def resolve_host(hostname: str) -> str:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [DNS_SERVER]
    try:
        fqdn = f"{hostname}.{DOMAIN}"
        answers = resolver.resolve(fqdn, "A")
        return str(answers[0])
    except Exception:
        return None

def main():
    print(f"[*] Querying authoritative DNS server ({DNS_SERVER}) for {DOMAIN} hosts...\n")
    inventory = {}
    for host in TARGET_HOSTS:
        ip = resolve_host(host)
        if ip:
            inventory[host] = ip
            print(f"    [DNS] {host}.{DOMAIN:<20} -> {ip}")

    print("\n[*] Transitioning to active TCP socket discovery...")
    for host, ip in inventory.items():
        print(f"\n--- Probing target: {host}.{DOMAIN} ({ip}) ---")
        open_count = 0
        for port in PORTS_TO_AUDIT:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((ip, port)) == 0:
                print(f"    [!] TCP Port {port} is OPEN")
                open_count += 1
            s.close()
        if open_count == 0:
            print("    [-] No target ports open or host not active.")

if __name__ == "__main__":
    main()
```

---

## 4. Step-by-Step Lab Execution

### Step 1: Start the Environment

From the host directory:

```bash
# Build attacker image and launch both containers
docker compose up -d --build

# Verify container statuses and IP assignments
docker compose ps
```

### Step 2: Access the Attacker Container

Open an interactive shell in `student-recon`:

```bash
docker exec -it student-recon /bin/bash
```

### Step 3: Run Reconnaissance and Scans

Inside the container:

```bash
# 1. Host discovery across the Docker subnet
python /app/01_ping_sweep.py 172.29.0.0/24

# 2. Audit the CoreDNS target directly
python /app/02_tcp_scanner.py 172.29.0.53

# 3. Banner grab against open services (e.g., DNS port 53)
python /app/03_banner_grabber.py 172.29.0.53 53

# 4. Run the end-to-end automated pipeline
python /app/04_recon_pipeline.py
```

### Step 4: Tear Down

When finished, shut down and remove the lab network from your host:

```bash
docker compose down
```











