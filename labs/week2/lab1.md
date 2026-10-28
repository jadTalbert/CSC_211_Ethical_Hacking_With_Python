# Week 2 Lab 1: Apply What You Have Learned

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T1079,T1619,T1119,T1070](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S0543,S0544,S0578,S0597,S0656,S0686,S0804](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K1079,K0677,K0679,K0682,K0684,K0688,K0710,K0751,K0752,K0779,K0882,K1182](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

---

### Overview & Objectives(Security & Client-Side Injection):
Apply your understanding of a White-Hat actor, RoE(Rules of Engagement) and reconnaissance(OSINT) from the lecture materials.

ACME Corp. was so impressed with your previous engagement and teamwork, they have renewed their security contract and asked that you return for this next effort---partnered with the same team as before. Your colleagues have been working diligently on a concern that was brought up by the lead Software Architect. He claims that the password strength of their Juice-Shop application is weak and will lead to potential bad actors using brute-force attacks to gain access to user accounts and data. This is the only problem he thinks the web site is vulnerable to and doesn't want you to review any other aspects of their implementation.

Your objective is to identify and recommend remediations based on your the following: 
- Reconnaissance(OSINT) efforts. 
- Scanning
- Vulnerability Analysis
- Exploitation
- Reporting & Remediation Findings


### Scenario 1:
One of your teammates was in a meeting with Ralph, the lead Software Architect, and they were told that the team just released a new search feature on the web site, and they are confident there are no security holes in their code and they insist you only focus on the weak password area of the web site.

Your teammates knows Ralph well, and are concerned with his arrogance around his team's abilties and knows from experience there are likely more vulnerabilites that have been introduced. Your teammates makes it clear to you that the team should focus on the search feature as well to ensure you are providing the service the Enterpise is paying for.

### Reconnaissance(OSINT) Findings:
After a few days of work, one of your teammates has found an OWASP top 10 vulnerability in Ralph's search feature. Your teammate provides you with the following HTML tag and wants you to confirm their findings by copying/pasting the HTML into the search box on the web site and executing a search. You should launch the [Juice-Shop](http://localhost:8080) web site on your local host and confirm their findings.

```json
<iframe src="javascript:alert('Hah! I hacked your search feature Ralph!')">
```

Another teammate found a similar problem in the same vein using HTML in the search box on the web site and asks that you copy/paste the HTML below and execute the search. After executing the search, you notice a form field with a submit button shows up as the search results. You in-turn enter some text in the form field and click the submit button.

```json
<form action="process.php" method="post" target="_blank">
  <label for="username">Name:</label>
  <input type="text" id="username" name="username">
  <input type="submit" value="Submit">
</form>
```

As your testing the search feature with the second vulnerability above, Ralph stops by and asks what you are doing, because their team noticed a lot of odd entries in the web server logs around a form named `process.php`. Their web site uses Angular and NOT PHP, so he's curious how this is happening because these requests are filling up their log files and reducing valuable disk space on their servers.

You launch your command line or terminal using `docker debug juice-shop` and type in the following command to watch the log files in real time:

#### NOTE: (you should use today's date in your log file name)
```tail -f logs/access.log.2026-10-28```

You see entries that Ralph is referring to and ask him---is this what you are seeing in the logs?

```
::ffff:192.168.65.1 - - [28/Oct/2026:03:32:05 +0000] "GET /process.php/socket.io/?EIO=4&transport=polling&t=k62zv7mo HTTP/1.1" 200 - "http://localhost:3000/process.php" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"
```

Ralph confirms---YES! Make it stop now, you're wreaking havoc on our site and affecting our customers!!

You must figure out how to stop the log entries quickly to avoid any further impact to the web site.

HINT: Keep watching the logs while you investigate. This will help let you know when the log entries stop occurring.


#### How To Submit This Lab:
- record a 3-5 minute video showing me the search vulnerability and how you solved the log entry problem that Ralph was so very concerned with.
- upload the video to Canvas.
- upload your vulnerability report to Canvas(e.g. same format as your week 1 assignments)



