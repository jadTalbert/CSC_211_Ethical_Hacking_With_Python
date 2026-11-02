
### Week 7 Lab 1: Reading, Parsing and Analyzing Log Files

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)


### Context
Due to your excellent work on the past engagements with ACME Corp. the CSO has established a new deparment and has asked you and your team to help her establish a new branch of the Network Security team to provide a wider range of talent to all of the security efforts needed.

You discuss this with your team and everyone is onboard with the request. Your new role starts today!

### Scenario 1:
Your new security team has identified what they belive to be possible attempts to subvert web server security. They noticed numerous entries in their main log file located at `/var/log/sample_logs/Linux2_k.log`  within the `forensics-lab` Docker container.

You should use the skills you have learned through past experience, to start the `forensics-lab` Docker container, connect to the running instance through VS Code and traverse the directory structure on the container to find the log `Linux2_k.log` file.

After finding the log file, you should write a python program to read the log file and count the number of `authentication failure` entries in the log file and group them by the date they occurred. 

<strong>Hint:</strong> Python3 is already installed on the Docker container

### Scenario 2:
Using the same python program, you should modify it to also search for `ALERT exited abnormally with [1]` entries and capture the date and time of the entry.

### Expected Output of python Programs for Scenarios 1 & 2:

| Failure Type   | Count | Date       |
| :------------- | :---- | :--------- |
| auth failures: | 10    | 10-10-2026 |
| auth failures: | 50    | 9-10-2026  |
| auth failures: | 3     | 8-10-2026  |
| auth failures: | 41    | 10-8-2026  |
| ALERT          | 90    | 9-10-2025  |
| ALERT          | 20    | 9-23-2025  |
| ALERT          | 43    | 7-11-2025  |

### How To Submit This Lab:
- Record a 2-3 minute video, showing me your working code running the Docker container
- Upload your python program to Canvas.
