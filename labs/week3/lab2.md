# Week 3 Lab2 Assignment: Active Reconnaissance(Direct Network Probing)

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-04,T-06,T-07,T-09,T-10,T-11,T-13,T-14,T-16,T1070,T1341,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-03,S-05,S-06,S-10,S-13,S-17,S-19,S0532,S0543,S0572,S0597,S0688](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-03,K-05,K-08,K-10,K0674,K0680,K0682,K0683,K0797,K0813,K0833,K0882,K0924,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

---

### Context
ACME Corporation was extremely pleased with your DNS assessment! They have decided to put Ralph on another team and have asked that your team lead the next round of vulnerability testing.

The CSO(Chief Security Officer) and CTO(Chief Technology Officer) are both concerned with the network posture of the company and want to do more active scanning to expose any potential risks within and around their network.

Both the CSO and CTO are still quite concerned about scanning their "real-World" physical network, so they have asked that you continue using the same Docker containers from the previous DNS passive scans.


### Subnet Target Map

| Target Hostname | Target IP | Record Type | Significance / Expected Findings |
| :--- | :--- | :--- | :--- |
| `ns1.acme-corp.com` | `172.29.0.53` | `A`, `SOA`, `NS` | Authoritative Name Server (TCP/UDP 53) |
| `mail.acme-corp.com` | `172.29.0.25` | `A`, `MX` | Mail exchange host (SMTP 25) |
| `vpn.acme-corp.com` | `172.29.0.16` | `A` | Remote access perimeter (OpenVPN / HTTPS) |
| `dev-api.acme-corp.com` | `172.29.0.101`| `A` | Pre-production internal API (Port 8080/3000) |
| `stage.acme-corp.com` | `172.29.0.102`| `A` | Internal staging web application (Port 80/8080) |
| `corp-db.acme-corp.com` | `172.29.0.200`| `A` | Backend database storage (MySQL/PostgreSQL) |

---

### Docker Container Updates Required:
One of your teammates stops you in the break room and tells you that they are in the process of configuring the Docker containers for the next round of scans, but will not have time to complete it today and asks you `is this ok?`. Your friendly response is `actually we have to get that done before end-of-day, so I'll take it and knock it out for you---no problem!`. 

After some research, you realize you need several Linux packages for network scanning and decide to install them running the script below, but before you can can run the scripts you have to connect to the `student-recon` docker container by entering the following command: `docker debug student-recon`

<strong>Hint:</strong> Use Copy/Paste to execute this in your container.

```bash
apt-get update && apt-get install -y --no-install-recommends \
    dnsutils \
    iputils-ping \
    net-tools \
    curl \
    nmap && \
pip install --no-cache-dir dnspython requests scapy
```

---

### Python Active Reconnaissance Scripts
After successfully installing the network utilities from the script above, you realize that you cannot figure out how to execute a python program from VS Code running on your local machine that will communicate with the docker container you are testing. 

So again, you go into research mode trying to figure this out and realize why you chose VS Code above all other IDEs---because it has great extensions and can do almost anything with them! So, you leap into action and install the `Dev Containers` VS Code extension.

After installing the `Docker Containers` extension, you finally find out how to use it by clicking the button with the two < > in the bottom left-hand side of VS Code.

<strong>Hint:</strong> See image below to launch Docker Containers from VS Code.

![launch docker container extension](./images/docker_container_extension.jpg)

Then you ask yourself....`wtf...which one do I choose?`. Fortunately, a Solution Architect on another team swings by your office to chat, and he can immedidately see you are stuggling and after explaining to him your situation, he says `pfft...that's easy dude, choose the running container that you are currently using, which should be the student-recon container.`.

<strong>Hint:</strong> See image below to choose the running container:

![choose running container](./images/docker_container_attach_to_running_container.jpg)

When a new VS Code window unexpectedly opens, you're asking yourself again `wtf is this?!!`. The same Solution Architect replies jokingly and says `that's VS Code attaching to Docker and now you can actually run your Python code directly on Docker using VS Code---that's fire right?`


---

### Executing The Python Script on Docker Using VS Code:

Realizing how simple this is now that you've had some help, you take the python script below, create a new file in your new VS Code window(e.g. the window attached to your `student-recon` Docker container) named `sweep.py`. 

```python
import ipaddress
import subprocess
import sys

def ping_host(ip: str) -> bool:
    """Send an ICMP echo request with a 1-second timeout."""
    cmd = ["ping", "-c", "1", "-W", "1", ip]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0

def sweep_network(subnet_cidr: str):
    print(f"[*] Starting host discovery sweep on {subnet_cidr}...Scanning 254 addresses\n")
    net = ipaddress.ip_network(subnet_cidr, strict=False)
    
    live_hosts = []
    for host in net.hosts():
        ip_str = str(host)
        
        
        if ping_host(ip_str):
            print("/"*43)
            print(f"//   \u2714 Live Host Detected: {ip_str}    //")
            print("/"*43)
            print("\r")
            live_hosts.append(ip_str)
        else:
            print(f"[x] No Host Detected at addresses {ip_str}...")
            
    print(f"\n[*] Sweep finished. {len(live_hosts)} active host(s) found.")
    return live_hosts

if __name__ == "__main__":
    target_subnet = sys.argv[1] if len(sys.argv) > 1 else "172.29.0.0/24"
    sweep_network(target_subnet)
```

Still in the VS Code window that is attached to your `student-recon` docker container, you open the VS Code terminal and type in the following command: `python3 sweep.py` and watch the code run.

While the code is executing the CSO stops by and asks `How's it going so far...any progress?`. You reply `I'm actually running my active ping testing now, and I'll update you as I know more.`

---

### How To Submit This Lab:
- Create a 2-3 minute video showing me that you can connect to your `student-recon` docker container and execute the `sweep.py` script inside the docker container successfully.
- Keep track of any findings or things you think are important,so that you can note them in the vulnerability report.



