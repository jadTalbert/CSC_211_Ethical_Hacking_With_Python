### Week 6 Lab 2: Deploying a Wifi Based QR Code

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-06,T-07,T-11,T-13,T-15,T-17,T1041,T1118,T1119,T1279,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-05,S-06,S-12,S0483,S0492,S0543,S0544,S0572,S0578,S0591,S0597,S0656,S0686,S0804](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-05,K-06,K-12,K-15,K-17,K0682,K0683,K0684,K0688,K0730,K0751,K0752,K0797,K0832,K0882,K0924,K0983,K1079,K1087,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)


### Context
With all of your White-Hat hacking experience, You are again working as an offensive security analyst for ACME Corp. with a defined RoE. You will be conducting a physical penetration test and awareness audit for a them because located next to their Corporate Headquarters is a well-known coffee shop with free WiFi.

Employees of ACME Corp. frequently work from the coffee shop, connecting their laptops and smartphones to a sticker on the counter reading:


<img src="../week6/images/scan_me.jpeg" alt="scan me" width="159" />

---

The CSO provides you the following details and reasoning behind this request:

```

 Instead of typing long SSIDs and passwords, 
 modern mobile devices (iOS and Android) support 
 native Wi-Fi configuration schemas embedded 
 directly into QR codes. When a phone camera scans 
 this format, the operating system bypasses the 
 browser completely and prompts the user. Because 
 users trust their device camera prompts far more 
 than suspicious web links, almost no one inspects
 what network they are actually joining.
 

```

Having already written another QR Code generator, you've got the technical chops to get this one done too, so quickly bang-out the program and start testing this on your home WiFi network to prove that it works.


---

```python
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image


def generate_wifi_payload(ssid: str, security: str, password: str, output_path: str):
 
    #Encodes Wi-Fi auto-connect schema:
    #Format: WIFI:S:<SSID>;T:<WPA|WEP|nopass>;P:<PASSWORD>;;
   
    payload = f"WIFI:S:{ssid};T:{security};P:{password};;"
    qr = qrcode.QRCode(
        version=4,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a1a1a", back_color="#ffffff")
    img.save(output_path)
    print(f"[+] Rogue Wi-Fi QR code saved to: {output_path}")


if __name__ == "__main__":

    generate_wifi_payload(
        ssid="Corporate_Executive_Guest",
        security="WPA",
        password="FreePublicInternetAccess!",
        output_path="rogue_wifi.png"
    )

```

### How To Submit This Lab:
- Record a 1-2 minute video showing me that you got this working. You should use VS Code to show the program compile and execute.
- Write up your vulnerability assessment with details to provide to the CSO with any concerns.












#### Objective
Students will create a lightweight Flask-based telemetry server (`quish_tracker.py`) simulating a credential harvester or canary token. When a target scans the QR code, the server captures client metadata (IP address, operating system, device family, user-agent) and immediately fires a terminal alert.

#### Python Implementation: `quish_tracker.py`
```python
"""
CSC-211: Lab 7.2 - QR Telemetry & Fingerprinting Listener
Captures connection headers, identifies client architecture, and logs scans.
"""

from flask import Flask, request, render_template_string
import datetime
import logging

app = Flask(__name__)

# Suppress default flask banner noise for clean logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

LANDING_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Factor Device Validation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 50px 20px; }
        .card { max-width: 400px; margin: auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h2 { color: #d9534f; }
        p { color: #555; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Identity Synchronized</h2>
        <p>Your mobile credentials have been verified by the security perimeter.</p>
        <p><small>Session ID: {{ token }}</small></p>
    </div>
</body>
</html>
"""

@app.route('/track/<token>')
def track_scan(token):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    accept_lang = request.headers.get('Accept-Language', 'Unknown')
    
    # Analyze device family from User-Agent string
    device_type = "Desktop / Generic"
    if "iPhone" in user_agent:
        device_type = "Apple iPhone (iOS Camera Scanner)"
    elif "Android" in user_agent:
        device_type = "Android Mobile Device"
    elif "iPad" in user_agent:
        device_type = "Apple iPad"

    print("\n" + "="*60)
    print(f"[!] ALERT: QR CODE SCANNED AT {timestamp}")
    print("="*60)
    print(f"[*] Target Token    : {token}")
    print(f"[*] Originating IP  : {client_ip}")
    print(f"[*] Inferred Device : {device_type}")
    print(f"[*] Full User-Agent : {user_agent}")
    print(f"[*] Language        : {accept_lang}")
    print("="*60 + "\n")

    return render_template_string(LANDING_PAGE, token=token)

if __name__ == "__main__":
    print("[*] Starting Quishing Telemetry Server on 0.0.0.0:5000...")
    print("[*] Point generated QR codes to: http://<YOUR_IP>:5000/track/<TOKEN>")
    app.run(host="0.0.0.0", port=5000, debug=False)
```

---






---

### Lab Steganographic Logo Overlay with Error Correction

#### Objective
Leveraging Reed-Solomon Error Correction Level H, modify the generated QR code to paste an opaque visual asset (e.g., an emblem or logo) covering the center $20\%$ of the image, proving that the code remains fully readable by mobile scanners despite physical data destruction.

#### Implementation Prompt & Code Skeleton: `qr_overlay.py`
```python
#!/usr/bin/env python3
"""
CSC-211: Lab 7.3 - Error-Tolerant Center-Badge Overlay
Demonstrates Reed-Solomon codeword resilience under physical image modification.
"""

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw

def create_resilient_badge_qr(data: str, output_file: str):
    # 1. Generate base QR code with maximum error correction (Level H = 30%)
    qr = qrcode.QRCode(
        version=4,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # 2. Calculate center coordinates
    qr_w, qr_h = qr_img.size
    box_size = qr_w // 4  # Target occupies 25% width
    
    box_x0 = (qr_w - box_size) // 2
    box_y0 = (qr_h - box_size) // 2
    box_x1 = box_x0 + box_size
    box_y1 = box_y0 + box_size

    # 3. Draw an opaque colored badge over the center modules
    draw = ImageDraw.Draw(qr_img)
    draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill="#c0392b", outline="#000000", width=3)
    
    # 4. Save and verify
    qr_img.save(output_file)
    print(f"[+] Resilient QR code with center badge generated: {output_file}")

if __name__ == "__main__":
    create_resilient_badge_qr("http://127.0.0.1:5000/track/EXECUTIVE_CANARY", "badge_qr.png")
```

---

## Lab Verification & Submission Requirements

1. **Working Code Submission:**
   * Submit `qr_generator.py`, `quish_tracker.py`, and `qr_overlay.py`.
2. **Execution Proof:**
   * Start `quish_tracker.py` on your machine.
   * Generate a QR code pointing to your local LAN IP (e.g., `http://192.168.1.X:5000/track/STUDENT_ID`).
   * Scan the physical screen using a smartphone camera.
   * Capture a screenshot of the terminal alert displaying the inferred mobile device family and parsed user agent.
3. **Critical Thinking Review Questions:**
   * Why do corporate email gateways that reliably catch raw URLs inside phishing emails frequently fail to detect the same malicious URLs encoded into an attached QR image?
   * If a QR code is generated with Error Correction Level L, what will happen if you attempt to place a company logo over the center modules? Explain using Reed-Solomon codeword principles.
   * What technical controls can mobile operating systems implement to mitigate URI scheme exploitation (such as silent auto-dialing or rogue Wi-Fi association)?