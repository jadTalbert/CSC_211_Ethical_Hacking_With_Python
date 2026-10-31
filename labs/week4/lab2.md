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

