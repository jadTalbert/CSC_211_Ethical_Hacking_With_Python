### Unsolicited vs. Solicited Banner Extraction

### Context

The CSO continually brags to the CTO about your teams abilities and how well you are performing the vulnerability assessments for ACME Corp. She knows that there are minor information vulnerabilities in terms of their Linux Operating Systems---specifically information displayed on banners when someone logs into a server. She makes the following statement to your team and wants you to perform another round of scans checking for banners.

```
Service banners themselves do not execute exploits, but in your ethical hacking efforts and penetration testing, they represent a significant information disclosure vulnerability (specifically categorized under CWE-200: Exposure of Sensitive Information). I need you to scan for banners an provide me the information your find in an report.

```

The CSO has provided some documentation listed below that you should review prior to starting your work.

#### Unsolicited Protocol Banners (Talkative Daemons)
Certain protocols are designed so the server transmits an informational greeting banner immediately upon socket connection, before the client sends any data:

* **SSH (RFC 4253):** The server immediately responds with its software version exchange string:
  ```text
  SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6
  ```
  *Analysis:* This single line reveals the protocol version (`SSH-2.0`), the software build (`OpenSSH 8.9p1`), the base operating system (`Ubuntu`), and the package build revision (`3ubuntu0.6`), which maps to a known upstream Linux kernel version.
* **FTP (RFC 959):** The server issues a numeric 220 status code:
  ```text
  220 (vsFTPd 3.0.3)
  ```
* **SMTP (RFC 5321):** Mail Transfer Agents announce their domain identity and server engine:
  ```text
  220 mail.internal-bank.com ESMTP Postfix (Ubuntu)
  ```


### Scanning for Banners(banner_grabber.py):
After your review of the CSO's information, she also mentions to you, that a python consultant was hired by the company and he has significant experience with using python as a tool for scanning ports. He has provided your team with a working version that he thinks will save you some time and effort. He asks that you review the code before executing it, to ensure it is what you need. He's not completely sure that it will work, so you should use the `cd ` command and change your directly to `week 4` in the cloned repository and execute the following command to start the container:

```docker compose --project-directory docker_files/ -f docker_files/docker-compose.yml up -d --force-recreate```

From your past experience with Docker containers, you realize that it's a good idea to use the copy/paste command `Ctrl+C` and `Ctrl+v` respectively to execture the command in the VS Code terminal.

Your experience has also taught you that you need to confirm the docker containers are running properly, so you execute the command below:

```
docker compose --project-directory docker_files/ -f docker_files/docker-compose.yml up -d --force-recreate
```

You expect the command to return the following three docker container names in the output:

```bash
coredns/coredns:latest
python:3.11-slim 
debian:bookworm-slim
```

```bash
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                                                                                                                                                                    NAMES
eea31d78ef08   coredns/coredns:latest   "/coredns -conf /etc…"   5 minutes ago   Up 5 minutes   0.0.0.0:1053->53/tcp, 0.0.0.0:1053->53/udp, [::]:1053->53/tcp, [::]:1053->53/udp                                                                                         acme-dns
8d59521a0bcb   python:3.11-slim         "sh -c 'pip install …"   5 minutes ago   Up 5 minutes                                                                                                                                                                         student-recon
df1611a3ebef   debian:bookworm-slim     "/bin/bash -c 'apt-g…"   5 minutes ago   Up 5 minutes   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp, 0.0.0.0:2222->22/tcp, [::]:2222->22/tcp, 0.0.0.0:2323->23/tcp, [::]:2323->23/tcp, 0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   victim-banner-server
```
 
After reviewing the python program below, you take this task on yourself and launch the `victim-banner-server` container using your previous knowledge about Docker and VS Code:

![launch docker container extension](./images/docker_container_extension.jpg)

![choose running container](./images/docker_container_attach_to_running_container.jpg)


```python
import socket
import sys

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    1194: "OpenVPN",
    3000: "Node / Dev Frontend",
    3306: "MySQL / MariaDB",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt / Dev-API",
    27017: "MongoDB"
}

def grab_banner(target_ip: str, port: int, timeout: float = 1.0) -> str:
    """
    Connects to an open port and extracts the initial service banner.
    Sends lightweight probes for protocols that do not transmit on connect.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((target_ip, port))

            # Protocols that expect a prompt before responding:
            if port in (80, 8080):
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            elif port == 6379:
                s.sendall(b"PING\r\n")

            # Receive raw banner bytes
            raw_data = s.recv(1024)
            if not raw_data:
                return "[No Banner Returned]"

            # Clean up whitespace and newlines for single-line display
            banner = raw_data.decode("utf-8", errors="ignore").strip()
            # If multi-line (e.g. HTTP headers), keep only the first relevant line
            first_line = banner.splitlines()[0] if banner else "[Empty Banner]"
            return first_line[:80]  # Cap width for neat terminal alignment

    except socket.timeout:
        return "[Banner Timeout]"
    except Exception as e:
        return f"[Banner Error: {e}]"

def scan_target(target_ip: str, ports: dict, timeout: float = 0.8):
    print(f"[*] Scanning Target: {target_ip}")
    print(f"{'PORT':<8} {'STATE':<8} {'SERVICE':<14} {'SERVICE BANNER'}")
    print("-" * 75)

    open_ports = []
    for port, service_hint in ports.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        result = s.connect_ex((target_ip, port))
        if result == 0:
            s.close()  # Close connection socket before banner grab
            banner = grab_banner(target_ip, port, timeout=1.0)
            print(f"{port:<8} {'OPEN':<8} {service_hint:<14} {banner}")
            open_ports.append((port, service_hint, banner))
        else:
            s.close()
        
    print("-" * 75)
    print(f"[*] Scan complete. Found {len(open_ports)} open port(s).")
    return open_ports

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "172.29.0.20"
    scan_target(target, COMMON_PORTS)

```

You quickly find that this is a very complicated python program and you are not exactly sure how it works---although it does work! In order for others to understand this code you pass the program to a colleague and ask them to properly comment the code, so that you can write the vulnerability report for this exercise.

### How To Submit This Lab:
- You should record a 1-2 minute video showing me the output of the python program running in the `victim-banner-server` docker image
- You should complete your assessment report as you have done in weeks past and upload it to Canvas.


#### Solicited Protocol Probing (Silent Daemons)
Modern services (especially web endpoints, RPC listeners, and databases) remain silent until receiving client data that matches their expected protocol structure:

* **HTTP/HTTPS Identification:** Probing web services requires constructing a valid application request. Sending an HTTP `HEAD` or `GET` request:
  ```http
  HEAD / HTTP/1.1\r\n
  Host: target-system\r\n
  User-Agent: Scanner/1.0\r\n
  \r\n
  ```
  Elicits headers that reveal application architectures:
  ```http
  HTTP/1.1 200 OK
  Server: Apache/2.4.52 (Unix) OpenSSL/1.1.1m
  X-Powered-By: PHP/8.1.2
  ```
* **Database & Binary Protocol Probing:** Databases like MySQL, Redis, or Microsoft SQL Server expect protocol-specific initialization sequences. Transmitting raw bytes such as `PING\r\n` to port 6379 checks for an unauthenticated Redis cache instance, which replies with `+PONG\r\n`.

### Operating System Fingerprinting via TCP/IP Stack Heuristics
When services suppress banner output (e.g., setting `ServerTokens Prod` in Apache or disabling banners in OpenSSH), scanners can identify the underlying operating system by analyzing **TCP/IP Stack Fingerprinting** anomalies.

Operating system vendors implement RFC specifications with subtle, deterministic differences:

1. **Initial Time-to-Live (TTL):** The 8-bit TTL field in the outbound IP header reveals the OS family. Windows kernels default to an initial TTL of **128**, Linux/Android kernels use **64**, and legacy Cisco/Unix architectures use **255**.
2. **Initial TCP Window Size:** The 16-bit Window Size field in an initial `SYN-ACK` reflects OS memory buffers. Linux systems often set this to `5840` or `29200`, whereas modern Windows environments select sizes like `8192` or `65535`.
3. **TCP Options Ordering & Support:** The combination and order of flags within the TCP Options field—such as Maximum Segment Size (MSS), Selective Acknowledgment (SACK Permitted), Timestamps (TSval/TSecr), and Window Scale factor—serve as a unique signature.
4. **DF (Don't Fragment) Bit Logic:** Modern Linux kernels set the DF bit to `1` by default on all transport frames to facilitate Path MTU Discovery, while certain embedded microcontrollers leave it unasserted (`0`).

```
+------------------+-------------------+----------------------+--------------------+
| Operating System | Default Initial   | Initial TCP Window   | Typical TCP Option |
| Platform         | IPv4 TTL          | Size Range           | Padding/Order      |
+------------------+-------------------+----------------------+--------------------+
| Linux Kernel 5.x | 64                | 29200 or 64240       | MSS, SACK, TS, WS  |
| Windows 10/11/Svr| 128               | 8192 or 65535        | MSS, NOP, WS, SACK |
| FreeBSD / macOS  | 64                | 65535                | MSS, NOP, WS, NOP  |
| Cisco IOS        | 255               | 4128                 | MSS                |
+------------------+-------------------+----------------------+--------------------+
```

---

