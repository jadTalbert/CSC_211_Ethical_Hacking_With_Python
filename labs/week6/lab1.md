
### Week 6 Lab 1: Assignment: QR Code Vulerabilities

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-06,T-07,T-11,T-13,T-15,T-17,T1041,T1118,T1119,T1279,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-02,S-05,S-06,S-12,S0483,S0492,S0543,S0544,S0572,S0578,S0591,S0597,S0656,S0686,S0804](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-02,K-05,K-06,K-12,K-15,K-17,K0682,K0683,K0684,K0688,K0730,K0751,K0752,K0797,K0832,K0882,K0924,K0983,K1079,K1087,](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)



### Context
With all of the success your team has had with ACME Corp. vulnerability scans, your team has experienced a small growth spurt and with new teammates, comes new ideas and a fresh perspective on security.

ACME Corp. is releasing a new product with QR codes printed directly on the packaging and the CSO has security concerns, because the product labels are created and printed in China. She is concerned that the label could be socially engineered to forward requests to a chinese owned domain before landing on the target domain(e.g. acme-corp.com). She expects you to confirm that her suspcisions are true in-terms of generating QR codes that can lead to bad actors capturing information they should not have access to.


With lots of new experience and ideas on your team, one colleague has built a well-defined set of Docker containers that will allow you to test this scenario. You ask this colleague to show you how to use the Docker containers and he tells, you that nothing has changed from your previous usage of Docker. So, all you have to do is `cd ` into the `week 6` directory and execute the following commands:

```bash
docker compose -f docker_files/docker-compose.yml down --remove-orphans

```

and

```bash
docker compose --project-directory docker_files/ -f docker_files/docker-compose.yml up -d --force-recreate
```

Knowing that Docker containers can fail to start up on occassion, you do the smart thing and check your work by executing `docker ps` to confirm that your have `python:3.11-slim and juice-shop:v14.5.1` docker containers running:

```bash
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS                  PORTS                                         NAMES
a2bd5c3661a7   python:3.11-slim                "sh -c 'pip install …"   10 seconds ago   Up 8 seconds                                                          workspace
96418b55fd5a   python:3.11-slim                "sh -c 'pip install …"   10 seconds ago   Up Less than a second   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   listener
f7ee1dce34dc   bkimminich/juice-shop:v14.5.1   "/nodejs/bin/node /j…"   10 seconds ago   Up 8 seconds            0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   target-app

```

After doing some research, you realize how simple it can be to generate QR codes, so you write the python program listed below to get things moving quickly.

However, you realize that if you want to scan a QR code on an external device such as your phone, you need to obtain your internal IP address. So, you execute the following in the VS Code terminal and use the internal IP address in your python program:

#### Mac/Linux
```bash
ifconfig en0
```

#### Windows
```bash
ipconfig | findstr /i "IPv4"

OR

ipconfig
```


### Lab: Programmatic QR Code Generation (`qr_code_generator.py`)

```python
import qrcode

# Point to the listener container IP with an open-redirect parameter
target_payload = "http://<yourInternalIPHere>:3000/?redirect=http://<yourInternalIPHere>:3000/#/login"

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(target_payload)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("malicious_portal_qr.png")
print("[+] QR Code written to malicious_portal_qr.png")

```

You should use the VS Code terminal to execute the program above directly from your local maching using the file name `qr_code_generator.py`.

You notice that the program generates a new image file named `malicious_portal_qr.png`, so you open the file in VS Code and use your phone to scan the QR code.

<strong>Hint:</strong> Using a Chrome or Edge browser may not work from your phone or other devices! You can use the [Brave Browser](https://brave.com/download/) instead.

After spending some time troubleshooting, you finally get this working(hopefully!) and realize just how dangerous QR codes can be. So, you write up your vulnerability assessment for the CSO as you have done in the past---using the same format.

### How To Submit This Lab:
- Record a 2-3 minute video, showing me the `docker ps` command and also, that you got the QR code scan working from your phone.
- Upload your vulnerability assessment to Canvas.






