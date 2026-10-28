# Offensive Security Field Guide: Web Application & Container Penetration Testing

**Classification:** White-Hat Assessment / Training Syllabus  
**Target Reference:** OWASP Juice Shop Containerized Environment (`bkimminich/juice-shop`)

---

## 1. Introduction: The Red-Team Mandate

In offensive security, a Red Team assessor emulates real-world threat actors to uncover weaknesses before adversaries exploit them. Unlike basic vulnerability scanning, an ethical hacking engagement follows a systematic, goal-oriented methodology. The objective is not simply generating finding counts, but assessing blast radius, privilege escalation paths, and defense-in-depth posture.

Modern web architectures rarely run bare-metal; they operate as decoupled Single Page Applications (SPAs) backed by microservices, runtime REST/GraphQL APIs, and containerized runtimes (Docker, Kubernetes). OWASP Juice Shop models this architecture accurately: an Angular frontend communicating with an Express/Node.js backend, writing to SQLite/Sequelize, wrapped in an OCI-compliant container image.

```
+--------------------------------------------------------------------------+
|                     Ethical Hacking Lifecycle                            |
|                                                                          |
|  Reconnaissance  -->  Discovery & Mapping  -->  Vulnerability Analysis   |
|          ^                                              |                |
|          |                                              v                |
|  Remediation/Retest <--  Reporting  <--  Post-Exploit / Escalation       |
+--------------------------------------------------------------------------+
```

---

## 2. Phase I: Passive & Active Reconnaissance

Every engagement begins with information gathering to define attack surfaces without alerting perimeter defenses prematurely.

### 2.1 Passive Surface Mapping
* **OSINT & Subdomain Enumeration:** Using passive discovery engines (Certificate Transparency logs, DNSdumpster, Amass) to locate staging, QA, and container registry endpoints.
* **Technology Fingerprinting:** Header inspections (`Server`, `X-Powered-By`) and public bundle scrapers indicate the underlying framework stack (e.g., Express, Angular, Webpack).

### 2.2 Active Enumeration & Content Discovery
* **Crawling & Endpoint Fuzzing:** Automated wordlist directory busting via `ffuf` or `gobuster` uncovers unlinked routing endpoints:
  ```bash
  ffuf -w /usr/share/wordlists/dirb/common.txt -u http://target:3000/FUZZ -mc 200,301,302,403
  ```
* **Client-Side Source Auditing:** In single-page architectures, build artifacts (`main.js`, `vendor.js`) often bundle unminified inline documentation, deprecated API routes, administrative endpoints, and environment paths. In Juice Shop, inspecting client JavaScript chunks reveals administrative paths like `/rest/admin` and hidden score-board mechanisms.

---

## 3. Phase II: Core Web Application Attack Vectors

Once mapped, the assessor systematically evaluates input vectors, state management, and API endpoints against the OWASP Top 10 vulnerabilities.

```
+-------------------+------------------------------------------------------+
| Attack Category   | Assessor Objective & Methodology                     |
+-------------------+------------------------------------------------------+
| Injection (SQLi)  | Break query contexts to extract data or bypass auth. |
| Broken Access     | Tamper with object IDs (IDOR), bypass role checks.   |
| Cryptographic     | Recover plaintext credentials from unsalted hashes.  |
| Client-Side (XSS) | Execute attacker payloads in user session contexts.  |
| API Logic Flaws   | Abuse mass assignment, rate limits, and zero-checks. |
+-------------------+------------------------------------------------------+
```

### 3.1 Authentication Bypass via Injection (SQLi)
Authentication interfaces accepting dynamic database queries without parameterized statements are primary targets for query structure disruption:
* **Vector:** Form fields, JSON authentication payloads, and header parameters.
* **Juice Shop Case Study:** The login endpoint evaluates input directly within an unparameterized SQLite string query. Submitting a structured tautology payload bypasses password checks:
  ```json
  POST /rest/user/login
  Content-Type: application/json

  {"email": "' OR 1=1--", "password": "arbitrary_value"}
  ```
  The SQL engine evaluates `WHERE email = '' OR 1=1--` to true, returning the initial index row (`id = 1`, the default administrator) and issuing an active JSON Web Token (JWT).

### 3.2 Insecure Direct Object References (IDOR) & Broken Access Controls
Modern APIs often decouple authorization checks from data query operations:
* **Methodology:** Capture authenticated requests using proxy tooling (Burp Suite, OWASP ZAP). Identify exposed identifiers (`userId`, `orderId`, `basketId`). Increment or substitute values across session tokens.
* **Juice Shop Application:** Modifying the `BasketId` inside persistent storage or request parameters allows an authenticated user to view, mutate, or empty another customer's shopping basket.

### 3.3 Client-Side Injection (Cross-Site Scripting - XSS)
Where input reflects into the DOM without sanitization, an attacker executes arbitrary code within victim browsers:
* **Reflected XSS:** Testing tracking and search fields with standard breakout strings (`<iframe src="javascript:alert(1)">`).
* **Stored / DOM XSS:** Submitting payloads within profile names, product reviews, or customer support forms to guarantee payload persistence across secondary administrative sessions.

---

## 4. Phase III: Escaping the Application to Container Infrastructure

When testing modern web targets, an application flaw can directly expose the container orchestration tier. A red-team assessor must evaluate whether web application compromise allows infrastructure compromise.

```
  [ Attacker ]
       |  (1. HTTP / Web Vulnerability)
       v
  +-------------------------------------------------+
  | Container Boundary                              |
  |  [ Web Service: Node / Express ]                |
  |         | (2. File Read / Command Execution)    |
  |         v                                       |
  |  [ Local SQLite File / System Environment ]     |
  +-------------------------------------------------+
       |  (3. Namespace Breakout / Sensitive Mount)
       v
  [ Host OS & Docker Daemon ]
```

### 4.1 Local Persistence Extraction
Juice Shop encapsulates its local SQLite store at `/juice-shop/data/juiceshop.sqlite`. Assessors targeting path traversal vulnerabilities (`../../`), Server-Side Request Forgery (SSRF), or container debugging access can inspect the raw database files:
* Extracting raw password values via strings inspection:
  ```bash
  strings /juice-shop/data/juiceshop.sqlite | grep -E "admin@" -A 1 -B 1
  ```
* This reveals unsalted MD5 hashes (`0192023a7bbd73250516f069df18b500`), which crack instantaneously against dictionary wordlists to reveal `admin123`.

### 4.2 Evaluating Container Privilege Boundaries
Container configurations frequently violate the principle of least privilege:
* **Root Execution Checks:** Verifying whether the container process runs under PID UID 0 inside its namespace.
* **Writable Mounts:** Checking if the host Docker socket (`/var/run/docker.sock`) is mounted into the container. An attacker with arbitrary code execution inside a container mounting the Docker socket can instantiate a privileged container over the host filesystem, resulting in total host compromise.
* **Information Leakage via Environment Variables:** Inspecting `/proc/1/environ` or running `env` within container execution vectors frequently exposes database connection strings, JWT signing keys, and cloud metadata tokens.

---

## 5. Phase IV: Defense-in-Depth & Mitigation Matrix

A professional red-team assessment concludes with remediation architecture rather than merely documenting exploitation paths.

| Target Layer | Attack Vector | Red-Team Proof-of-Concept | Secure Implementation Fix |
| :--- | :--- | :--- | :--- |
| **API Layer** | SQL Injection | `' OR 1=1--` on login | Utilize parameterized queries / ORM prepared statements (e.g., Sequelize bind parameters). |
| **Identity** | Weak Hash Reversal | Offline cracking of MD5 user hashes | Implement Argon2id or bcrypt ($2b$ with cost factor $\ge 12$) with unique salts. |
| **Client** | Stored/DOM XSS | Injection into user feedback form | Sanitize and contextualize output encoding; enforce Strict Content Security Policy (`CSP`). |
| **Container** | Host Escape / Dump | Extraction of SQLite via unprivileged container exec | Run rootless containers (`USER nonroot`), mount read-only filesystems, avoid exposing host sockets. |

---

## 6. Summary Checklist for Ethical Red-Team Operators

1. **Adhere to ROE (Rules of Engagement):** Confirm scope, target CIDRs, test accounts, and rate-limiting thresholds before running active fuzzing.
2. **Log Every Payload:** Retain complete HTTP proxy history and terminal logs with timestamps to assist the Blue Team in log-correlation and telemetry validation.
3. **Validate Business Impact:** Pivot from simple technical triggers (e.g., triggering an `alert(1)`) to demonstrating tangible business risk (e.g., accessing unauthorized customer PII).
4. **Deliver Clear Remediation:** Equip engineering teams with precise reproduction steps, patch examples, and retest verification criteria.