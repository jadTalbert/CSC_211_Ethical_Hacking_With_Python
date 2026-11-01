# Week 6 Lecture Physical-Digital Attack Vectors — Malicious QR Codes & Client-Side Delivery

**Course:** CSC-211 Ethical Hacking with Python  
**Module:** Physical-to-Digital Pivoting, QR Code Exploitation, and Client Delivery  
**Prerequisites:** Familiarity with Python HTTP requests, basic socket concepts, and Flask web routing.

---

## Lecture & Conceptual Foundations

### The Physical-to-Digital Bridge
In traditional network exploitation, the attack surface begins at exposed internet ports, misconfigured cloud interfaces, or perimeter services. Physical-digital attack vectors invert this model: they rely on physical objects (printed paper, signage, badges, decals, or packaging) to induce a human target to execute code or transmit sensitive state across the network.

Quick Response (QR) codes are two-dimensional matrix barcodes invented in 1994 by Denso Wave. While initially designed for high-speed industrial parts tracking, modern mobile operating systems (iOS and Android) have integrated automatic QR parsing into default camera firmware. 

When a smartphone lens encounters a QR pattern, the operating system decodes the matrix, interprets the encoded Uniform Resource Identifier (URI) or plain string, and prompts the user—often automatically pre-fetching data, parsing metadata, or offering single-tap actions. This seamless convenience strips away the user's defensive scrutiny, turning visual cues into an unauthenticated entry point.

---

### QR Code Internal Architecture & Encoding Mechanics

To audit or weaponize QR codes in red teaming, an ethical hacker must understand their structural anatomy:

```
+-----------------------------------------------------------------------+
|                         QR CODE ANATOMY DIAGRAM                       |
|                                                                       |
|   [Finder Pattern]                [Timing Pattern]  [Finder Pattern]  |
|    +---------+                     . . . . . . .     +---------+      |
|    | +-----+ |                                       | +-----+ |      |
|    | |     | |                                       | |     | |      |
|    | +-----+ |                                       | +-----+ |      |
|    +---------+                                       +---------+      |
|                                                                       |
|    [Format Info]                   [DATA AREA]       [Format Info]    |
|                                     Encoded Bytes                     |
|                                    Reed-Solomon EC                    |
|                                                                       |
|    +---------+                     [Alignment Pattern]                |
|    | +-----+ |                        +---+                           |
|    | |     | |                        +---+                           |
|    | +-----+ |                                                        |
|    +---------+                                                        |
|   [Finder Pattern]                                                    |
+-----------------------------------------------------------------------+
```

#### Core Components
1. **Finder Patterns:** The three nested square targets located at the top-left, top-right, and bottom-left corners. These enable camera optical sensors to detect the matrix, calculate orientation, and adjust for physical distortion/perspective angles.
2. **Alignment & Timing Patterns:** Embedded grid lines that establish coordinate tracking across larger code matrices.
3. **Format Information:** Identifies the error correction level and the data mask applied to ensure balanced module (black/white dot) distribution.
4. **Data Modules & Error Correction:** The payload area containing binary data interleaved with Reed-Solomon error correction codewords.

#### Versions and Capacity
* QR codes scale from **Version 1** ($21 \times 21$ modules) up to **Version 40** ($177 \times 177$ modules).
* Capacity depends on the encoding mode: Numeric (up to 7,089 characters), Alphanumeric (4,296 characters), Byte (2,953 8-bit bytes), and Kanji (1,817 characters).

#### Reed-Solomon Error Correction (ECC)
QR codes employ mathematical redundancy allowing recovery if the matrix is damaged, obscured, or overlaid:
* **Level L (Low):** $\approx 7\%$ of codewords can be restored.
* **Level M (Medium):** $\approx 15\%$ restored.
* **Level Q (Quartile):** $\approx 25\%$ restored.
* **Level H (High):** $\approx 30\%$ restored.

**Offensive & Red-Team Relevance:** Level H allows an attacker to paste deceptive corporate logos, security badges, or misleading text directly over up to $30\%$ of the barcode without breaking readability. The scanner successfully reconstructs the underlying payload despite visual occlusion.

---

### Attack Surfaces & Exploitation Vectors

```
                                  [Physical Scanned Code]
                                             |
            +--------------------------------+--------------------------------+
            |                                |                                |
            ▼                                ▼                                ▼
  [Standard Web URLs]               [URI Scheme Abuse]               [QRLJacking / Auth]
   - Quishing (Phishing)             - WIFI: (Auto-join rogue AP)     - Session Relay
   - Parameter tampering (OAuth)     - tel: (Auto-dial premium)       - Fake 2FA prompts
   - Exploit payload delivery        - smsto: / facetime:             - QR login hijack
```

#### A. "Quishing" (QR Phishing) & Reverse Proxy Harvest
Because users cannot read raw 2D pixel matrices with the naked eye, they cannot spot typosquatted domains (`paypa1.com`), deceptive path structures, or malicious subdomains. Furthermore:
* Traditional Email Security Gateways (ESGs) inspect text bodies and hyperlinks, but often pass image attachments without running optical character recognition (OCR) or QR decoding.
* Attackers place the QR code inside a PDF invoice or security alert. The user scans it with a mobile device, bypassing all corporate endpoint monitoring, firewall inspection, and web proxy filters installed on their workstation.

#### B. URI Scheme Abuse (Direct Device Interaction)
Mobile operating systems register specific URI handlers that execute distinct actions:
* **Wi-Fi Auto-Configuration:** `WIFI:S:GuestWiFi;T:WPA;P:CorpSecretPass;;` — Forces or prompts the device to immediately authenticate to a rogue access point (Evil Twin), facilitating downstream Man-in-the-Middle (MitM) attacks.
* **Telephony & Messaging:** `tel:*21*5551234#` (triggering unconditional call forwarding) or `smsto:12345:PAY_AUTH` (authorizing micro-transactions).
* **Intent/Deep-Linking:** Triggering internal mobile application screens via registered application schemes (e.g., `bankapp://transfer?to=attacker&amount=1000`).

#### C. QRLJacking (Quick Response Login Jacking)
Many modern applications (WhatsApp Web, Discord, Telegram, and banking platforms) offer "Scan to Login" functionality:
1. The server generates a dynamic QR code displaying a transient cryptographic authentication session token.
2. The user scans the code using an already-authenticated mobile app to validate their desktop session.
3. **The Attack:** An attacker runs an automated script that fetches the real server's dynamic QR code, mirrors it onto a phishing page in real time, and tricks an unsuspecting user into scanning it. Once the victim scans the mirrored code, they authenticate the attacker’s browser session.

---

