# CSC-211: Ethical Hacking with Python
## Lecture: Network Reconnaissance & Custom Port Scanning

---

### Course & Module Information
* **Course:** CSC-211 (Ethical Hacking with Python)
* **Module:** Network Reconnaissance, Transport Layer Probing, and Service Enumeration
* **Prerequisite Knowledge:** TCP/IP 4-Layer Model, RFC 793 Fundamentals, Basic Linux CLI
* **Target Competency:** Deconstruct scanning mechanics at the byte, packet, and transport layers to prepare for custom Python scanner architecture.

---

## 1. Reconnaissance Methodologies: Active vs. Passive Scanning

Reconnaissance represents Phase 1 of the Ethical Hacking Lifecycle. Its objective is to map target footprints, isolate network perimeters, enumerate responsive hosts, and catalog exposed application interfaces. 

Offensive and defensive security teams classify reconnaissance into two operational modes: **Passive Information Gathering** and **Active Network Scanning**. The distinction centers on packet telemetry, legal boundaries, detection risks, and transport-layer physics.

```
+---------------------------------------------------------------------------------------+
|                                RECONNAISSANCE SPECTRUM                                |
+---------------------------------------------------+-----------------------------------+
|               PASSIVE RECONNAISSANCE              |        ACTIVE RECONNAISSANCE      |
+---------------------------------------------------+-----------------------------------+
|  Target Interaction: Indirect / Zero Packets Sent |  Target Interaction: Direct Packets  |
|  Telemetry: Logged on Third-Party Systems         |  Telemetry: Logged on Target IDS/IPS |
|  Legal Exposure: Public Intelligence Querying     |  Legal Exposure: Explicit Rules of Eng|
|  Tools/Protocols: DNS, BGP, WHOIS, CT Logs, OSINT |  Tools/Protocols: ICMP, TCP, UDP, ARP |
+---------------------------------------------------+-----------------------------------+
```

### 1.1 Passive Reconnaissance (Out-of-Band Intelligence)
Passive reconnaissance aggregates intelligence without transmitting a single data frame, packet, or segment to the target infrastructure. Attackers query intermediate third-party brokers, public archives, and distributed cache infrastructure.

* **DNS Forward/Reverse Harvesting & Cache Inspection:** Passive DNS mapping tracks hostnames and historical IP address allocations without sending DNS queries directly to the target’s authoritative name server. Threat actors inspect Certificate Transparency (CT) logs (`crt.sh`, Google Transparency Report) to uncover subdomains (e.g., `dev-vpn.internal.corp`, `staging-api.corp`) generated during TLS certificate issuance.
* **Autonomous System Number (ASN) & BGP Route Graphing:** Attackers isolate IP address ownership blocks by analyzing Border Gateway Protocol (BGP) routing tables through looking-glass servers. Querying Regional Internet Registries (RIRs: ARIN, RIPE, APNIC) via WHOIS and RDAP establishes network perimeter limits and identifies netblocks, colocation arrangements, and cloud tenant boundaries.
* **Search Engine & Sensor Telemetry (OSINT):** Querying internet-wide historical scanning engines (Shodan, Censys, Criminal IP) reveals open ports, previously discovered web servers, cryptographic keys, and outdated banners captured days or weeks prior.
* **Operational Profile & Legal Context:** Passive intelligence gathering leaves zero logs in the target's Security Information and Event Management (SIEM) systems or local host firewalls. It falls under standard public data consumption, making it legally distinct from probing private digital infrastructure. However, passive data suffers from cache decay, latency, and stale network state.

### 1.2 Active Reconnaissance (Direct Network Probing)
Active reconnaissance transmits synthetic network traffic directly to the target's routable addresses. Its goal is to elicit deterministic network-layer (ICMP/ARP) and transport-layer (TCP/UDP) responses to determine if a host is alive and what services are actively listening.

* **Network-Layer Host Discovery:** Before scanning 65,535 ports on a host, active discovery checks whether an IP address is reachable. Techniques include:
  * **ARP Sweeps:** On local broadcast segments (Layer 2), sending `who-has` frames identifies hosts instantly regardless of host-based firewalls, as hosts must resolve ARP to communicate.
  * **ICMP Echo / Timestamp / Address Mask Probing:** RFC 792 ICMP Type 8 (Echo Request) probes elicit Type 0 (Echo Reply). Modern enterprise firewalls and host operating systems (e.g., Windows Firewall default rules) routinely drop ICMP Type 8, necessitating transport-layer pinging.
  * **Transport Pings (TCP ACK/SYN to common ports):** Transmitting naked `ACK` segments to port 80 or 443 forces an active host’s TCP/IP stack to return an unprompted `RST` segment (RFC 793), confirming host vitality even when ICMP is completely blocked.
* **The Noise Factor & Operational Hazard:** Active reconnaissance touches the target's operating perimeter. Every dropped packet, rejected connection, or malformed frame generates audit entries across edge stateful firewalls, Intrusion Detection Systems (IDS like Snort/Suricata), and Network Security Monitoring (NSM) sensors. Active scanning requires explicit authorization under a formal Rules of Engagement (RoE) contract.

---

## 2. Full TCP Connect Scans vs. Half-Open SYN Stealth Scans

Port scanning is the systematic transmission of connection packets across transport-layer endpoints (0–65535) to identify service states: **Open**, **Closed**, or **Filtered**. The two most fundamental scanning strategies are the **Full TCP Connect Scan** and the **Half-Open (SYN) Stealth Scan**.

```
  TCP CONNECT SCAN (Standard 3-Way Handshake + Clean Teardown)
  
      Scanner                                                Target
         |                     1. [SYN]                        |
         | --------------------------------------------------> |  OS Kernel completes
         |                 2. [SYN, ACK]                       |  connection and passes
         | <-------------------------------------------------- |  socket to user space!
         |                     3. [ACK]                        |
         | --------------------------------------------------> |
         |                   4. [RST, ACK]                     |
         | --------------------------------------------------> |

  -----------------------------------------------------------------------------

  TCP HALF-OPEN SYN SCAN (Kernel Interruption / Raw Socket Injection)
  
      Scanner                                                Target
         |                     1. [SYN]                        |
         | --------------------------------------------------> |  Target reserves state;
         |                 2. [SYN, ACK]                       |  Daemon never sees
         | <-------------------------------------------------- |  connection established.
         |                     3. [RST]                        |
         | --------------------------------------------------> |  Connection torn down
                                                                  immediately!
```

### 2.1 State-Transition Mechanics & RFC 793 Protocol Logic

A target TCP stack acts as a finite state machine. How it responds to an inbound segment reveals the state of the probed port:

| Port State | Received Probe | Target TCP Stack Response | RFC 793 Conformance Behavior |
| :--- | :--- | :--- | :--- |
| **Open** | `SYN` | `SYN, ACK` (Synchronize-Acknowledge) | Stack acknowledges sequence number; allocates Transmission Control Block (TCB). |
| **Closed** | `SYN` | `RST, ACK` (Reset-Acknowledge) | Stack rejects connection immediately; no application is bound to the port. |
| **Filtered** | `SYN` | *No Response* (Drop) or *ICMP Type 3* | Firewall silently drops segment or issues ICMP Type 3 (Destination Unreachable) Code 1, 2, 3, 9, 10, or 13. |

### 2.2 Full TCP Connect Scans (`connect()`)
In a full TCP connect scan, the scanner relies entirely on the operating system’s underlying network subsystem to complete the full RFC 793 three-way handshake: $\text{SYN} \to \text{SYN-ACK} \to \text{ACK}$.

1. **System Execution:** The scanning utility calls the standard operating system socket API (`connect()`).
2. **Kernel Handshake Completion:** The local OS kernel generates the initial `SYN` packet. Upon receiving `SYN-ACK`, the local kernel handles sequence numbers and automatically dispatches the completing `ACK` packet. The TCP connection reaches the `ESTABLISHED` state.
3. **Application Layer Handoff:** Once `ESTABLISHED`, the target OS kernel notifies the listening daemon via the `accept()` system call. The connection is entered into the service's active connection table.
4. **Immediate Teardown:** The scanner closes the socketDescriptor, issuing a `FIN` or `RST` to cleanly terminate the session.

#### Operational & Engineering Trade-Offs
* **Privilege Independence:** Full connect scans run inside user space without elevated root or administrative capabilities (`CAP_NET_RAW` on Linux or `sudo` on macOS).
* **Network & Endpoint Logging:** Because the three-way handshake completes, listening services (e.g., Apache, Nginx, OpenSSH, PostgreSQL) register an established connection. Even if terminated before sending application data, an entry (e.g., *"Connection reset by peer"* or a blank HTTP connection) is written to application logs (`/var/log/nginx/access.log`, `auth.log`).
* **Resource Cost & Overhead:** Establishing and tearing down full TCP state machines incurs higher latency and memory overhead on both the scanning engine and intermediate firewalls.

### 2.3 Half-Open SYN Stealth Scans
The half-open scan—often called a SYN scan or stealth scan—bypasses the operating system's standard transport-layer abstraction. It gathers port state information without ever completing the three-way handshake.

1. **Synthetic Transmission:** The scanner manually crafts an IP packet encapsulating a TCP header with only the `SYN` flag bit set (`0x02`), transmitting it via a raw network socket.
2. **Triage of Inbound Frame:** 
   * If the target responds with `SYN-ACK` (`0x12`), the port is verified as **Open**.
   * If the target responds with `RST-ACK` (`0x14`), the port is verified as **Closed**.
3. **The Half-Open Reset:** Upon receiving the `SYN-ACK`, the scanner *never* sends the final `ACK`. Instead, it transmits an unsolicited `RST` (`0x04`) segment directly back to the target.
4. **State Machine Abortion:** The target OS receives the `RST` segment and immediately invalidates its embryonic half-open connection (TCB allocation). 

#### Operational & Engineering Trade-Offs
* **Application Daemon Stealth:** Because the connection never achieves the `ESTABLISHED` state, the target operating system's kernel drops the connection without notifying the user-space process. The web server, SSH daemon, or database server never executes `accept()`, leaving zero transaction trails in application-level logs.
* **Privilege Demands:** Creating raw Ethernet frames or raw IP packets bypasses normal OS TCP state tracking. This requires root permissions (`sudo` or system administrator privileges) on the scanning host.
* **Network Device Detection:** While stealthy against application logs, SYN scans are an explicit signature for Network Intrusion Detection Systems (NIDS). A sudden burst of naked SYN packets followed immediately by RST packets from the same source IP will trigger automated alerts and IP blocking rules across modern firewalls.

---

## 3. Service Banner Grabbing and Fingerprinting Open Ports

Identifying that a TCP port is open provides only transport-layer state. Security analysts must identify the software running on that port, including the server application, exact version string, underlying operating system, and patch level. This process is called **Service Enumeration and Fingerprinting**.

```
+---------------------------------------------------------------------------------------+
|                         APPLICATION FINGERPRINTING METHODS                            |
+---------------------------------------------------+-----------------------------------+
|              UNSOLICITED BANNER GRAB              |      SOLICITED PROTOCOL PROBING   |
+---------------------------------------------------+-----------------------------------+
|  Behavior: Listener talks first upon connect.     |  Behavior: Listener waits silently for input.|
|  Method: Open socket -> Read buffer immediately.  |  Method: Send format probe -> Parse reply.|
|  Protocols: SSH, FTP, SMTP, POP3, Telnet          |  Protocols: HTTP, HTTPS, TLS, SMB, RPC|
|  Payload Sent: None (0 bytes)                     |  Payload Sent: "HEAD / HTTP/1.1\r\n\r\n"|
+---------------------------------------------------+-----------------------------------+
```

