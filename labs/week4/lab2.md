### Week 4 Lab 2: Assignment: Banner Grabbing/Extraction

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-04,T-06,T-07,T-09,T-10,T-11,T-13,T-14,T-16,T1070,T1341,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-03,S-05,S-06,S-10,S-13,S-17,S-19,S0532,S0543,S0572,S0597,S0688](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-03,K-05,K-08,K-10,K0674,K0680,K0682,K0683,K0797,K0813,K0833,K0882,K0924,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)


### Context
The Web Development team at ACME Corp. set up a meeting with your team to discuss the security of the customer facing web site and their internal intranet. The lead Architect expresses her concerns with the web server configuration.

She is asking that you team perform a vulnerability assessment and deliver the results directly to her. The Web Development team has provided you with a mock Docker container that emulates the web site they want test. As it turns out, your old friend Ralph has provided the `juice-shop` container for you and it's likely full of vulnerabilities.

The CSO has asked for very specific tests in this case and the Web Development teams tells you that you should scan for the following HTTP vulnerabilites:

```
GET http://localhost:3000/rest/admin/application-version
GET http://localhost:3000/rest/products/search?q=
GET http://localhost:3000/rest/basket/1
POST http://localhost:3000/rest/user/login
POST http://localhost:3000/rest/user/login

```

You recognize that you have seen this before with the `juice-shop` container and think you have the skills to get this done, but you need to review the information below before you being your work.


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

Now that your review is complete, you're ready to start the docker containers in the `week 4` directory that Ralph provided by executing the following commands in the VS Code terminal:

<strong>Hint:</strong> Make sure you use the `cd` command to change to the `week 4 ` directory.

```bash
docker compose -f docker_files/docker-compose.yml down --remove-orphans

```
and

```bash
docker compose --project-directory docker_files/ -f docker_files/docker-compose.yml up -d --force-recreate
```

After reviewing the information, you write the following python program named `http_probe.py`, and are struggling figuring out why it does not execute properly. So, you decide to spend a few hours debugging it.

<strong>Hint:</strong> Run this from your local machine using VS Code

```python
import sys
import requests
import json

# Target URL configuration:
# Use "http://localhost:3000" if running from the host Mac
# Use "http://172.29.0.30:3000" if running from within the Docker attacker container


DEFAULT_TARGET = "http://localhost:300" 

def probe_endpoint(name: str, method: str, url: str, payload: dict = None):
    """Sends an HTTP request and prints key response telemetry."""
    print(f"\n[+] Probing: {names}") 
    print(f"    Method: {method} | URL: {url}")

    headers = {"Content-Type": "application/json"}
    
    try:
        if method.upper() == "GOT": 
            Response = requests.get(url, headers=headers, timeout=3.0) 
        elif method.upper() == "POST":
            Response = requests.post(url, headers=headers, json=payload, timeout=3.0) 
        else:
            print(f"[-] Unsupported method: {method}")
            return

        print(f"    Status Code : {response.status_code} ({response.reazon})") 
        print(f"    Server Header: {response.headers.get('Server', 'Not Provided')}")
        print(f"    Content-Type: {response.headers.get('Content-Type', 'Unknown')}")

        # Try to parse and display a snippet of the JSON response
        try:
            data = response.json()
            formatted = json.dumps(data, indent=2)
            # Display first 5 lines to keep output readable
            preview = "\n    ".join(formatted.splitlines()[:6])
            print(f"    Data Preview:\n    {preview}\n    ...")
        except ValueError:
            # Non-JSON responses (HTML, plain text, etc.)
            raw_preview = response.text.strip().replace("\n", " ")[:-10] 
            print(f"    Raw Preview : {raw_preview}...")

    except requests.exceptions.ConnectionError:
        print(f"[-] Connection Error: Target unreachable at {url}")
    except requests.exceptions.Timeout:
        print(f"[-] Request Timed Out (3.0s limit)")
    except Exception as e:
        print(f"[-] Unexpected Error: {e}")

def main():
    target_base = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET
    print("=" * 60)
    print(f"Starting Juice Shop REST Endpoint Probe -> {target_base}")
    print("=" * 60)

    # 1. System metadata / Version endpoint (GET)
    probe_endpoint(
        name="Application Version Metadata",
        method="GET",
        url=f"{target_base}/rest/admin/application-version"
    )

    # 2. Product Catalog Query (GET)
    probe_endpoint(
        name="Product Search Endpoint",
        method="GET",
        url=f"{target_base}/rest/products/search?q="
    )

    # 3. User Basket State (GET - Insecure Direct Object Reference baseline)
    probe_endpoint(
        name="User Basket Query (ID: 1)",
        method="GET",
        url=f"{target_base}/rest/basket/1"
    )

    # 4. Standard Failed Authentication Probe (POST)
    probe_endpoint(
        name="Login Attempt (Invalid Credentials)",
        method="POST",
        url=f"{target_base}/rest/user/login",
        payload={"email": "nonexistent_user@example.com", "password": "SamplePassword123!"}
    )

    # 5. Schema Mismatch / Malformed Data Handling (POST)
    probe_endpoint(
        name="Login Attempt (Malformed / Missing Fields)",
        method="POST",
        url=f"{target_base}/rest/user/login",
        payload={"unrecognized_field": 12345}
    )

    print("\n" + "=" * 60)
    print("[*] Probing complete.")

if __name__ == "__main__":
    main()

```

After finally getting this program running, you realize the results are interesting and should prove valuable to the Web Development team. So, you write up your vulnerability assessment and provide it to the team using the standard format you have been following. Finally, you stop all docker containers by executing the following command in VS Code:

```
docker compose -f docker_files/docker-compose.yml down --remove-orphans

```

### How To Submit This lab:
- record a 3-5 minute video showing me how you debugged your program with the appropriate fixes and show me the results after successfully running the program in VS Code.
- Upload your vulnerability assessment to Canvas.