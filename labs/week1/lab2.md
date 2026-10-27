# Week 1 Lab 2: Apply What You Have Learned

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-xx](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-xx](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-xx](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

---

### Overview & Objectives:
Apply your understanding of a White-Hat actor, RoE(Rules of Engagement) and reconnaissance(OSINT) from the lecture materials.

ACME Corp. has agreed to hire you as a security consultant and Ethical Hacker. Your company has all of the required documentation for the Operational Diminsion of this project, which means that you have a signed, legally binding contract and Rules of Engagement (RoE) for this operation. 

Your objective for this engagement is to secure the enterprise, mitigate business risk and protect users.

Based on previous reconnaissance from one of your colleages, it was found that user passwords were stored in plain-text on the file system. Using your White-Hat Hacking skills, execute the following docker command on your command line or terminal

`docker debug juice-shop`

Next, your colleague has an emergency family matter and cannot continue working on the problem. However, they have created a simple script they believe will help you. They ask you to copy/paste the following command at the `docker > ` prompt and continue without them for the time-being.


```strings /juice-shop/data/juiceshop.sqlite | grep -C 5 "admin@juice-sh.op"```

You should read through the information printed to the console and note ALL identified email addresses that are listed and save this to your computer for use in your final report.

Shortly after you executed the previous commands, another colleague tells you that they think they found the file that contains plain-text passwords, and they need you to investigate to confirm their findings.

They ask you to execute the following command using `docker debug`

`vi data/static/users.yml`

<strong style="color:red;">Note:</strong> `vi` (short for VIM) is a Linux text editor, so when you done with your evaluation of the `users.yml` file, type the following in the command line while the file is open:

`:q!`  This will close the file without writing any accidental changes you may have made.
    

You should review the output from the command and either confirm or reject their findings in your report and provide the following information for the `admin` user from the `users.yml` file:

    - email
    - password
    - role
    - credit card number(s)
    - all address information

---

### Confirmation of Your Findings

To confirm your findings, go to `http://localhost:3000` and login using the administrator credentials(e.g. email address & password). If this works(and it should!), your findings are confirmed!

You should review the example remediation report below and complete this with your detailed findings. This report should be complete and accurate based on your findings. If remediation has not yet been implemented, you should note this in your report and let the enterprise know you will re-evaluate once fixes have been put into place by their development team.

<strong style="color:red;">Note:</strong>  Your role is the White-Hat Ethical Hacker, not the developer that fixes the vulnerabilties, so the fix is not your responsibility!

---

### Vulnerability Remediation Summary Report

### Assessment Metadata

| Field | Details |
| :--- | :--- |
| **Target Application** | Juice Shop (`xx.x`) |
| **Assessment Type** | Web Application Plain-Text password vulnerability|
| **Initial Assessment Date** | <date of report here>|
| **Remediation Retest Date** | <date of remediation here> |
| **Lead Security Assessor** | <your name here> |


---

### Example Executive Summary

During the penetration testing assessment conducted on October 20, 2026, multiple vulnerabilities were identified spanning insecure credential storage, exposure of administrative identities in local databases, and missing container-level access restrictions. 

This document details the **remediation status** of all identified vulnerabilities following corrective actions deployed by the engineering team. Of the **3 vulnerabilities identified**, **2 have been successfully remediated**, and **1 has been mitigated with a compensating control** pending architectural refactoring.

All critical and high-severity risks directly compromising authentication integrity have been resolved. The remaining medium-severity finding is protected by runtime sandboxing and permission hardening until a scheduled database engine migration in Q1 2027.

---

### Example Remediation Status Overview

| Finding ID | Vulnerability Title | Original Severity | Current Status | Verification Date |
| :--- | :--- | :--- | :--- | :--- |
| **VULN-01** | Weak Password Hashing Algorithm (Unsalted MD5) | **High** (CVSS 7.5) | **Remediated** | Oct 27, 2026 |
| **VULN-02** | Hardcoded Default Administrative Credentials in Codebase | **Critical** (CVSS 9.1) | **Remediated** | Oct 27, 2026 |
| **VULN-03** | Insecure Local SQLite Storage Permissions inside Container | **Medium** (CVSS 5.3) | **Mitigated (In Progress)** | Oct 27, 2026 |

### How To Submit This Lab:
- record a 2-3 minute video showing and explaining in your own words the following:
    - open the users.yml file `vi data/static/users.yml`
    - show me how you identified the admin information for this vulnerability(e.g. username, password, credit card etc.) in the users.yml file.
    - launch the juice-shop website on your machine and enter the admin username(email) and password and login.
    - upload your detailed remediation overview to Canvas

