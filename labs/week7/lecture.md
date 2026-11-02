# Week 7 Lecture: Remote Access Mechanics, Detection, and Log Forensics

---

## Remote Access Architectures

In network security and systems administration, remote access channels allow administrators—or unauthorized operators—to execute commands on a host from across a network. Understanding how these communication channels operate at the transport and operating system layers is essential for designing effective network boundaries, monitoring telemetry, and analyzing intrusions.

### Ingress vs. Egress Communication Models

Remote interactive sessions fundamentally rely on standard TCP/IP socket connections, categorized by which endpoint initiates the handshake:

* **Bind Shell Architecture (Inbound / Ingress):**
  * **Mechanism:** A process on the target machine opens a listening socket on a designated port (e.g., TCP 4444) and attaches the input/output streams of a command interpreter (such as `/bin/sh` or `cmd.exe`) to that socket. The connecting client initiates the TCP handshake to the target host's IP address.
  * **Network Constraints:** In modern network environments, firewalls, stateful packet filters, and Network Address Translation (NAT) gateways almost universally block unsolicited incoming connections from the outside. Unless port forwarding is configured or the target resides directly on a public IP without host-based firewalls, bind channels fail at the perimeter.

* **Reverse Shell Architecture (Outbound / Egress):**
  * **Mechanism:** The target host acts as the network client, initiating an outbound connection to an external listener managed by the operator. Once the TCP three-way handshake completes, the target host binds its command interpreter's input/output to this established outbound connection.
  * **Network Realities:** Firewalls are typically configured with permissive egress filtering, allowing internal systems to establish outbound connections on standard ports (such as HTTP/80, HTTPS/443, or DNS/53) to access web resources. Because stateful firewalls track TCP connection states, return traffic across an established outbound connection is permitted through the boundary.

```
Bind Architecture:
[Client / Operator] ──(Inbound TCP SYN)──> [Firewall / NAT] ──X (Dropped)──> [Target Listener]

Reverse Architecture:
[Operator Listener] <──(Outbound TCP SYN)── [Permitted Egress] <────────────── [Target Host]
```

### Operating System Process Plumbing: Standard I/O Redirection

At the operating system level, an interactive shell session requires three standard streams (file descriptors in POSIX environments):
* `stdin` (File Descriptor 0): Standard Input
* `stdout` (File Descriptor 1): Standard Output
* `stderr` (File Descriptor 2): Standard Error

When a local terminal starts a shell, these descriptors point to the terminal driver (`/dev/pts/*`). In a programmatic remote access channel, the process redirects these streams through the network socket using kernel system calls:

1. **Socket Allocation:** The process instantiates a standard network socket (`int sockfd = socket(...)`).
2. **Connection Establishment:** The socket connects out to the designated destination IP and port (`connect(sockfd, ...)`).
3. **Descriptor Duplication (`dup2`):** The process duplicates the socket descriptor over `0`, `1`, and `2`:
   ```c
   dup2(sockfd, 0); // Redirect stdin to socket
   dup2(sockfd, 1); // Redirect stdout to socket
   dup2(sockfd, 2); // Redirect stderr to socket
   ```
4. **Execution (`execve`):** The process replaces its execution image with a shell (`/bin/sh`). Any byte received over the TCP stream is treated as standard keyboard input, and any output or error messages written by executed programs are transmitted back through the socket.

---

## Detection Strategies and Host Artifacts

Understanding the mechanics of remote access reveals the physical footprints left behind on host endpoints and network sensors.

### Process Lineage and Behavioral Anomalies

In legitimate operations, command interpreters are spawned by parent processes associated with user sessions—such as `login`, `sshd`, a desktop display manager, or a scheduled cron daemon. 

* **Anomalous Parentage:** If an interactive shell (`sh`, `bash`, `powershell.exe`) has a web application runtime or server process (such as `www-data`, `nginx`, `apache2`, `node`, or a database service) as its direct parent, this represents a severe behavioral anomaly. Web servers serve HTTP requests; they rarely spawn interactive command shells under normal business logic.
* **Socket Inspection:** Using native utilities such as `ss` (Socket Statistics), `netstat`, or `lsof`, analysts can correlate active network connections with running Process IDs (PIDs):
  ```bash
  # List established TCP sockets with associated process binaries and PIDs
  ss -tupn state established
  ```
  An established outbound connection originating from a process with no valid remote sync requirement (e.g., `/bin/bash` communicating with an unknown external IP over non-standard ports) is a high-confidence indicator of compromise.

---

## Web and Application Log Forensics

Before an adversary obtains remote access on an application host, they typically perform reconnaissance, scanning, and exploitation phases. These activities generate extensive forensic artifacts in web server access and error logs.

### Understanding Common Log Formats (CLF and Combined)

Standard web servers (Nginx, Apache, Caddy) record ingress HTTP transactions in structured formats, most commonly the NCSA Combined Log Format:

```text
Log Format Specification:
%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"

Example Entry:
198.51.100.23 - - [01/Nov/2026:14:22:10 -0500] "GET /admin/login.php HTTP/1.1" 404 287 "-" "python-requests/2.31.0"
```

Each field serves a specific forensic purpose:
* **Client IP (`%h`):** Source IP address of the requester (or the last proxy hop).
* **Timestamp (`%t`):** Date and time of the event, critical for building timelines and correlating across systems.
* **Request Line (`"%r"`):** The HTTP verb, requested URI, and protocol version.
* **Status Code (`%>s`):** The server response code (e.g., `200` OK, `403` Forbidden, `404` Not Found, `500` Internal Server Error).
* **Bytes Sent (`%b`):** Size of the response payload, useful for identifying data exfiltration or anomalous responses.
* **User-Agent (`"%{User-Agent}i"`):** The declared identity of the client client/library.

### High-Value Forensic Indicators

When investigating access logs for automated activity or reconnaissance, security teams look for distinct analytical markers:

1. **Automation Signatures in User-Agents:**
   Standard development and automation libraries include default identifier strings unless developers explicitly override them. Common indicators include:
   * `python-requests/*`, `Python-urllib/*`
   * `curl/*`, `Wget/*`
   * Vulnerability scanner banners (`Nikto`, `sqlmap`, `nmap`)

2. **High-Frequency Request Clustering (Burst Analysis):**
   Human browsing generates variable inter-request delays (think time) accompanied by secondary requests for static assets (`.css`, `.js`, images). Automated directory enumerators (e.g., scanning for sensitive directories like `/.env`, `/backup.sql`, `/admin`) produce dozens or hundreds of requests per second, often focused entirely on unlinked paths.

3. **Status Code Ratio Anomalies:**
   Under normal usage, the vast majority of web requests return successful status codes (`200`, `301`, `304`). A sharp increase in `404 Not Found` or `403 Forbidden` responses from a single IP indicates systematic brute-forcing or path fuzzing.

4. **Payload Injection Artifacts in URIs:**
   URI queries containing shell metacharacters (`;`, `|`, `&`, `$(...)`), path traversal sequences (`../../`), or directory references (`/bin/sh`, `/etc/passwd`) reveal attempts to achieve code injection.

---

## Methodological Framework for Log Ingestion

When writing automated forensic ingestion tools in Python, analysts structure their parsing pipelines into three core stages:

```
[ Ingestion & Normalization ] ──> [ Feature Extraction ] ──> [ Aggregation & Scoring ]
```

1. **Ingestion & Normalization:** Read the raw log stream line-by-line using regular expressions to safely unpack structured tokens without throwing runtime exceptions on malformed rows.
2. **Feature Extraction:** Convert string timestamps into comparable datetime objects, parse query strings, and categorize HTTP response ranges.
3. **Aggregation & Scoring:** Group records by entity (primarily Source IP), calculating metrics such as:
   * Total request count vs. unique paths hit.
   * Error rate percentage ($\frac{\text{Status } 4xx}{\text{Total Requests}}$).
   * Presence of known non-browser User-Agent strings.

Entities that exceed established statistical baselines are flagged for investigation, firewall rule updates, or incident escalation.