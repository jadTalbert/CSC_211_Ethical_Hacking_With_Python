# Lab Assignment: Passive Reconnaissance & Attack Surface Mapping

**Course:** CSC-211 (Ethical Hacking with Python)  
**Target Entity:** ACME Corporation (`acme-corp.com` / sandbox target)  
**Engagement Type:** Red Team Operations (Phase 1: Passive Reconnaissance)  
**Deliverables:** Functional Python Script (`passive_recon.py`), Executive Summary, and Vulnerability Assessment Report  

---

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

---
### Context
ACME Corporation has contracted your red team to evaluate their internet-facing exposure prior to an upcoming major platform release. Company leadership is concerned that forgotten staging/testing servers, misconfigured DNS zone settings, and administrative test endpoints are readily discoverable by external adversaries.


ssh into container: docker compose exec -it attacker /bin/bash
or
docker debug

next, pip install dnspython requests on your local machine, so that it can talk to docker container

---
---
--- 

MAY NOT KEEP THIS!!!!!

## 1. Scenario & Rules of Engagement (RoE)

### 1.1 Context
ACME Corporation has contracted your red team to evaluate their internet-facing exposure prior to an upcoming major platform release. Company leadership is concerned that forgotten staging servers, misconfigured DNS zone settings, and administrative test endpoints are readily discoverable by external adversaries.

### 1.2 Rules of Engagement (RoE) Parameters
* **Scope Definition:** Primary registered domain `acme-corp.com` (for classroom/lab testing, substitute a designated sandbox domain such as `example.com` or your team's assigned host).
* **Operational Mode:** **Strictly Passive.** No direct packets, TCP handshakes, ICMP pings, or HTTP requests may be sent to ACME Corporation’s actual web servers, network firewalls, or hosting infrastructure.
* **Authorized Data Sources:** Third-party intermediaries and public aggregators only:
  * Public Certificate Transparency (CT) log indexes (e.g., `crt.sh`).
  * Public recursive DNS resolvers (querying authoritative records out-of-band).
  * Regional Internet Registry (RIR) WHOIS and RDAP records.
* **Primary Objective:** Enumerate discoverable subdomains, catalog mail exchange (MX) and name server (NS) configurations, inspect SPF/TXT policy disclosures, identify potential high-value targets (e.g., `dev`, `vpn`, `stage`), and compile findings into an executive report.

---

## 2. Python 3 Starter Script: `passive_recon.py`

This starter script queries the public **Certificate Transparency (crt.sh)** JSON endpoint and executes out-of-band DNS lookups using `dnspython`. It interacts solely with third-party aggregators and resolvers, satisfying the passive constraint of the RoE.

### 2.1 Dependencies
Install the required packages in your Python virtual environment:

```bash
pip install dnspython requests
```

### 2.2 Script Source Code

```python
#!/usr/bin/env python3
"""
CSC-211: Passive Reconnaissance Starter Script
Target: ACME Corporation
Method: Certificate Transparency (crt.sh) & Public DNS Querying
"""

import json
import re
import sys
import dns.resolver
import requests

def get_subdomains_crtsh(domain: str) -> list:
    """
    Harvests subdomains passively via Certificate Transparency logs (crt.sh).
    Zero direct packets are sent to the target's web infrastructure.
    """
    print(f"[*] Querying Certificate Transparency logs for: {domain}...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            records = response.json()
            for entry in records:
                name_value = entry.get("name_value", "")
                # crt.sh may return newline-delimited entries and wildcard entries
                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()
                    if sub.startswith("*."):
                        sub = sub[2:]
                    if sub.endswith(domain) and sub != domain:
                        subdomains.add(sub)
        else:
            print(f"[-] crt.sh returned HTTP status {response.status_code}")
    except requests.exceptions.RequestException as exc:
        print(f"[-] Error querying crt.sh API: {exc}")

    return sorted(list(subdomains))

def query_dns_records(domain: str):
    """
    Queries common public DNS records (A, MX, NS, TXT) using standard resolvers.
    """
    print(f"\n[*] Enumerating public DNS records for: {domain}")
    record_types = ["A", "MX", "NS", "TXT"]

    for r_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, r_type)
            print(f"\n[+] {r_type} Records:")
            for rdata in answers:
                print(f"    - {rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"[-] No {r_type} records found.")
        except dns.resolver.NXDOMAIN:
            print(f"[-] Domain {domain} does not exist.")
            break
        except Exception as exc:
            print(f"[-] Error resolving {r_type}: {exc}")

def analyze_subdomain_exposure(subdomains: list):
    """
    Resolves discovered subdomains to inspect IP mapping and highlight
    high-value target patterns (e.g., dev, test, vpn, staging, admin).
    """
    print(f"\n[*] Resolving Discovered Subdomains ({len(subdomains)} unique entries):")
    risky_keywords = ["dev", "test", "stage", "staging", "admin", "vpn", "corp", "internal", "api"]

    for sub in subdomains:
        flagged = any(kw in sub for kw in risky_keywords)
        flag_label = " [!] HIGH-VALUE TARGET" if flagged else ""

        try:
            answers = dns.resolver.resolve(sub, "A")
            ips = ", ".join([rdata.to_text() for rdata in answers])
            print(f"    - {sub:<35} -> {ips}{flag_label}")
        except Exception:
            # Subdomain in CT log may no longer resolve (stale certificate)
            print(f"    - {sub:<35} -> [Unresolved / Stale Record]{flag_label}")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <domain>")
        print(f"Example: python3 {sys.argv[0]} acme-corp.com")
        sys.exit(1)

    target_domain = sys.argv[1].strip().lower()
    print("=" * 65)
    print(f"  CSC-211 PASSIVE RECONNAISSANCE SCANNER: {target_domain.upper()}")
    print("=" * 65)

    # Step 1: Query CT Logs
    discovered_subdomains = get_subdomains_crtsh(target_domain)

    # Step 2: Query Baseline DNS Records
    query_dns_records(target_domain)

    # Step 3: Analyze Subdomain Attack Surface
    if discovered_subdomains:
        analyze_subdomain_exposure(discovered_subdomains)
    else:
        print("\n[-] No subdomains discovered via public Certificate Transparency.")

    print("\n[+] Passive reconnaissance phase complete. Output ready for reporting.")

if __name__ == "__main__":
    main()
```

---

## 3. Deliverable Templates for Students

Students are required to format their engagement results into the following two report sections.

### Section A: Executive Summary

```markdown
# Executive Summary: External Attack Surface & Passive Assessment

**Target Organization:** ACME Corporation  
**Assessor:** Red Team Assessment Group (CSC-211)  
**Date:** October 28, 2026  
**Engagement Type:** Passive Reconnaissance (Out-of-Band Analysis)  

### 1. Assessment Overview
From October 26 to October 28, 2026, the Red Team performed a zero-impact passive reconnaissance assessment against ACME Corporation's registered domain perimeter (`acme-corp.com`). The goal was to quantify external attack surface exposure using publicly indexed Certificate Transparency logs and third-party recursive DNS resolvers without transmitting direct network traffic to ACME Corporation’s systems.

### 2. High-Level Findings
1. **Exposure of Pre-Production Infrastructure:** Certificate logs catalog multiple development and staging endpoints (`dev-api.acme-corp.com`, `vpn-test.acme-corp.com`) resolving to public IP space alongside production systems.
2. **DNS & Email Policy Weaknesses:** The current SPF TXT record configuration employs a soft-fail (`~all`) mechanism and includes overly broad address blocks, creating opportunities for domain spoofing.
3. **Orphaned / Stale Pointers:** Several subdomains indexed in public certificates failed to resolve or point to unallocated third-party cloud assets, creating potential subdomain takeover risks.

### 3. Attack Surface Metrics
* **Total Discovered Subdomains:** 14
* **High-Value / Sensitive Endpoints Identified:** 5
* **Actionable Vulnerabilities Documented:** 3
```

---

### Section B: Vulnerability Assessment Report

| Finding ID | Title | Severity | Impact Summary | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| **VULN-PASS-01** | Public Visibility of Pre-Production Subdomains via Certificate Logs | **Medium** | Staging endpoints (`stage-app`, `dev-api`) expose unfinished authentication mechanisms and internal application paths to external adversaries. | Implement split-horizon DNS; do not register public wildcard or domain certificates for internal-only hostnames on public root domains. |
| **VULN-PASS-02** | Permissive SPF Record Configuration (`~all` / Overly Broad IP Ranges) | **Low** | The current TXT SPF record contains broad `/24` subnet masks and a soft-fail (`~all`), facilitating potential email spoofing and domain reputation degradation. | Tighten SPF definitions to authorized mail gateways; transition the final directive from `~all` to `-all` (hard fail); prune legacy IP addresses. |
| **VULN-PASS-03** | Stale DNS Pointer Records (Potential Subdomain Takeover) | **Medium** | Two discovered subdomains resolve to third-party cloud hosting endpoints (AWS S3 / CNAME) that return 404 or unallocated statuses. | Audit external DNS CNAME records; remove orphaned pointers immediately to prevent adversaries from claiming abandoned cloud buckets or hosts. |

---

## 4. Student Submission Checklist

1. **Working Code:** Execute `passive_recon.py` against the assigned target domain and ensure output completes without uncaught exceptions.
2. **Raw Log File:** Save standard output to `recon_output.txt`:
   ```bash
   python3 passive_recon.py <assigned-domain> > recon_output.txt
   ```
3. **Completed Report:** Fill out the Executive Summary and Vulnerability Table with concrete findings, evidence strings, and tailored remediation steps based on your actual recon output.