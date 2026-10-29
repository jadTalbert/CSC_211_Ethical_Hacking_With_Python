# Lab Assignment: Passive Reconnaissance & Attack Surface Mapping

**Course:** CSC-211 (Ethical Hacking with Python)  
**Target Entity:** ACME Corporation (`acme-corp.com` / sandbox target)  
**Engagement Type:** Red Team Operations (Phase 1: Passive Reconnaissance)  
**Deliverables:** Functional Python Script (`passive_recon.py`), Executive Summary, and Vulnerability Assessment Report  

---

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-04,T-06,T-07,T-09,T-10,T-11,T-13,T-14,T-16,T1070,T1341,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-03,S-05,S-06,S-10,S-13,S-17,S-19,S0532,S0543,S0572,S0597,S0688](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

---
### Context
ACME Corporation has contracted your red team to evaluate their internet-facing exposure prior to an upcoming major platform release. Company leadership is concerned that forgotten staging/testing servers, misconfigured DNS zone settings, and administrative test endpoints are readily discoverable by external adversaries.

### Scenario 1:
You guessed it....Ralph is back in action. The CSO discovered that Ralph's team yet again has generated serious concerns among upper management at ACME Corp. It turns out his team executed untested penetration scripts and brought down the company web site around 2am this morning for a 2 hour outage window. The estimated cost of this downtime was around $425,000 USD.


The CSO has now dictated to all technial teams, including yours, that nothing can directly access production systems without first being tested in docker containers to ensure proper vetting has occurred. All teams must prove their work and the CSO has hired an outside firm to provide a properly configured set of docker containers for you to use.

Due to the ongoing concerns with Ralph's team, you must use the pre-configured Docker containers for your vulnerability assessment and the outside firm has also provided a Github repository for you to use that contains the Docker configuration.

### Step 1:(Cloning the Github Repository)
- Clone the [CSC-211 Github Repository](https://github.com/jadTalbert/CSC_211_Ethical_Hacking_With_Python) if you have not already done so.
- If you have already cloned it, make sure you pull the latest changes to your local host using VS Code.
- In VS Code, open the terminal and use the `cd ` (cd stands for change directory) command to change to the `week 3` directory.
    - Example of using the `cd` command: `cd CSC_211_Ethical_Hacking_With_Python/labs/week3`. Note, that this is an example, your local machine may have a different path.
- Using the VS Code terminal type in the following command: `pwd`. This prints the working directory---hence `pwd`. You should be in the `week3` directory. If not, use the `cd` command mentioned earlier and make sure you are in the correct directory. <strong style="color:red;">THIS IS CRITICALLY IMPORTANT!</strong>

### Step 2: (Using the New Docker Containers):
Since the docker containers have been pre-designed for you by an outside firm, this makes things much easier to test your passive scans.

- Using the VS Code terminal, copy/paste the command below and execute the command:

    `docker compose --project-directory docker_files/  -f docker_files/docker-compose.yml up -d`

An initial start-up that shows an error may require running another command to remove orphaned containers:

```
[+] up 2/3
 ✔ Network docker_files_recon-net Created                                                                                                    
 ✔ Container student-recon        Started                                                                                                  
 ⠹ Container acme-dns             Starting                                                                                                    
Error response from daemon: failed to set up container networking: Address already in use
```


If you receive an error when the containers attempt to start, you should execute the following command:

<strong style="color:red;">!!!ONLY EXECUTE IF YOU RECEIVE ERRORS!!!!</strong>

```
docker compose -f docker_files/docker-compose.yml down --remove-orphans

```
A successful start up looks something like this:
```
    [+] up 2/2
    ✔ Container student-recon Started 
    ✔ Container acme-dns      Started 
 ```



After your containers are started, you should execute the following command in the VS Code terminal to confirm the containers are working:

`docker ps`

You should now see two containers running with the following image names:
` python:3.11-slim` and `coredns/coredns:latest`



### Step 3: Stopping the Docker Container(s):
<strong>Note:</strong> This step is optional and here for your reference if you need to stop and restart your containers.

To stop your containers, copy/paste the following command in the VS Code terminal:

```
docker compose --project-directory docker_files/  -f docker_files/docker-compose.yml down
```

You can restart your containers anytime by running:

```
docker compose --project-directory docker_files/ -f docker_files/docker-compose.yml up -d
```

---

### Step 4: Installing Dependencies On Your Local Machine
Using the VS Code terminal, type in the following command:

```bash
pip install dnspython requests
```

This installs the requisite dependencies on your local machine that you will need to for DNS(Domain Name Service) passive scanning.


At this point, the CSO is satisfied that your team has been briefed on the new approach and has the necessary tools for the next round of vulnerabilty scanning---she asks you to get started immediately!


### Reconnaissance: Passive DNS Scanning

---

#### Rules of Engagement (RoE) Parameters
* **Scope Definition:** Primary registered domain `acme-corp.com`.
* **Operational Mode:** **Strictly Passive.** No direct packets, TCP handshakes, ICMP pings, or HTTP requests may be sent to ACME Corporation’s actual web servers, network firewalls, or hosting infrastructure.
* **Authorized Data Sources:** Pre-configured Docker containers are to be used to vet vulnerabilities.
* **Primary Objective:** Enumerate discoverable subdomains, catalog mail exchange (MX) and name server (NS) configurations, inspect TXT records and high-value targets (e.g., `dev.acme-corp.com`, `vpn.acme-corp.com`, `stage.acme-corp.com`), and compile findings into an executive report.
---


<strong>Note:</strong> The consultant that configured the docker containers for you knows that ACME Corp.'s public DNS A record is `acme-corp.com` and has configured this ahead of time.

Using VS Code, you will passively scan the DNS docker container for specific information. The python script you will execute is below. You should use VS Code and copy/paste the code below into a new file named `passive_dns_scan.py` and execute the program using the following command on the VS Code terminal: `python3 passive_dns_scan.py`

```python
import dns.resolver

# Initialize a custom resolver targeting our container mapped port
custom_resolver = dns.resolver.Resolver()
custom_resolver.nameservers = ["127.0.0.1"]
custom_resolver.port = 1053

# DNS set up for query execution
domain = "acme-corp.com"
for rtype in ["A", "MX", "TXT"]:
    try:
        answers = custom_resolver.resolve(domain, rtype)
        print(f"[+] {rtype} records for {domain}:")
        for rdata in answers:
            print(f"    - {rdata.to_text()}")
    except Exception as e:
        print(f"[-] {rtype} lookup failed: {e}")
```

After executing the program, you provide the results to another member on your team and ask them to issue a vulnerability assessment on your findings. The next day, your colleague comes to you makes the following statement:
```
I have no idea how to read and understand what you gave me---it's just not something I know very well. Can you provide me some insight on the topic of DNS?
```

You let your colleague know that you're new to this as well, and will be happy to do some additional digging on DNS. For the final vulnerability assessment report, you decide to use Google's Gemini AI platform to research DNS record types A, MX and TXT and have the AI platform explain in detail what DNS is and the difference between the A, MX and TXT records.

---



### How To Submit This Lab:
- record a 3-5 minute video showing me that you have successfully created the two Docker containers by executing `docker ps`. You should also show me that you can execute the python code and explain the differences in A, MX and TXT DNS records. Upload your video to Canvas.
