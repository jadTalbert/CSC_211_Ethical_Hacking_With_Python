### Week 6 Lab 3: Understanding Moving QR Codes

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-06,T-07,T-11,T-13,T-15,T-17,T1041,T1118,T1119,T1279,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-05,S-06,S-12,S0483,S0492,S0543,S0544,S0572,S0578,S0591,S0597,S0656,S0686,S0804](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-05,K-06,K-12,K-15,K-17,K0682,K0683,K0684,K0688,K0730,K0751,K0752,K0797,K0832,K0882,K0924,K0983,K1079,K1087,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)


### Context
ACME Corp. has decided to sell tickets to their annual conference in San Diego California before the end of their fiscal quarter. This event is a major contributor to their marketing efforts and rasises awareness around their Global product offerings. 

The CSO has already been getting calls about the scalpers from last year's event and that over 100 fake tickets have been sold to unsuspecting customers attending the event, which ultimately denied them entry into the conference. This in-turn reduced customer confidence and the CSO is demanding that your team prototype a QR Code scanning system that changes in real-time to avoid anyone taking pictures of a static QR code and using them at the ticket gate.


### CSO Reasoning and Research

The CSO spent a lot of time researching the importance of moving QR codes and the underlying threat and secuirty aspects. She has provided the following infomraiton for you to review.

Moving (or dynamic, rolling) QR codes are more secure primarily because they introduce ephemerality (time-based validity),functioning much like a Time-Based One-Time Password (TOTP) or cryptographic nonce.


#### Why They Are More Secure
Eliminates Replay and Screenshot Attacks: A static QR code can be photographed, screenshotted, or printed, allowing an attacker to reuse or distribute it indefinitely. A moving QR code encodes a short-lived token (valid for only 5–30 seconds); once expired, any captured image is cryptographically invalid.

#### Prevents Credential and Ticket Scalping/Theft: 
In high-value access environments (event ticketing, transit passes, facility badges), dynamic rolling codes ensure that only the person in active possession of the authorized app or authenticated session can present a valid scan.

#### Thwarts Man-in-the-Middle (MitM) Interception: 
Even if network telemetry or an over-the-shoulder snapshot captures the raw payload, the time window to replay the payload to the verifying server is typically too narrow to exploit.

#### Why They Are Useful
Physical Access Control & Badging: Replaces static keycards or printed barcodes in enterprise environments, preventing employees or visitors from sharing or duplicating entry credentials.

#### High-Value Live Ticketing: 
Used by platforms like Ticketmaster ("SafeTix") and airlines to defeat duplicate ticketing fraud, barcode scalping, and fraudulent resale.

#### Out-of-Band Authentication & Login: 
Provides a frictionless, phishing-resistant alternative for desktop logins (e.g., scanning a web portal code with a mobile banking app) by embedding a one-time session handshake directly into the moving image.


### Lab Assignment:
After reviewing the CSO's materials and overall request, you used ChatGPT to generate a functional version of a prototype to test. Your teammates took it upon themselves to modify the program, but they have introduced defects and are having problems getting the code to work. They have asked that you debug the program, and once you have it running, you should using your mobile phone to test the moving QR code to confirm it does change with each rotation.


```python
import time
import uuid
import qrcode

def generate_rolling_token_qr():
    while True:
        # Generate an ephemeral session token / timestamp
        #session_token = str(uuid.uuid4())[:8] 
        ephemeral_url = session_token

        qr == qrcode.QRCode(box_size=1, border=1)
        qr.add_data(ephemeral_url)
        qr.make(fit=True)

        # Clear terminal screen (works on macOS / Linux)
        print("\033[H\033[J", end="")
        print(f"=== Active Auth Token: {session_token} (Refreshes in 5s) ===")
        
        # Render directly in terminal using ASCII blocks
        qr.print_ascii(invert=True)
        
        time.sleep(5)

if __name__ == "__main__":
    generate_rolling_token_q()

```

### How To Submit This Lab:
- Record a 2-3 minute video showing me how you fixed the defects in the program, and that the program works properly. Specifically, shoiwng the QR code rotates every 5 seconds.
- Write up your report to show the CSO this prototype could actually work for her needs. You may use generative AI to assist you with writing the report(note: this is not a vulnerability assessment, but a basic write-up of your findings). Upload your findings to Canvas.