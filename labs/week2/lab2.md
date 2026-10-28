# Week 2 Lab 2: Apply What You Have Learned

#### [NICE Framework Reference](https://github.com/jadTalbert/NICE_Framework/)

- Role: [JRT-1](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/roles/roles.md)
- Tasks: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/tasks/tasks.md)
- Skills: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/skills/skills.md)
- Knowledge: [](https://github.com/jadTalbert/NICE_Framework/blob/main/NICE_Framework/knowledge/knowledge.md)



### Overview & Objectives:(Security & SQL Injection)
Apply your understanding of a White-Hat actor, RoE(Rules of Engagement) and reconnaissance(OSINT) from the lecture materials.


One of ACME Corp.'s customers created a support ticket stating the email address that was used when creating their account was not correct and it needs to be fixed immediately because they cannot login to the Web Site. More specifically the customer claims that their email address on file is: `john.q.public@`.

### Scenario 1:

<strong style="color:red;">Note:</strong> Make sure your Juice-Shop docker container is running by executing the `docker ps` command on the command line or terminal.

During your reconnaissance(OSINT) efforts, you test the [Juice-Shop](https://localhost:8080/#/register) web site on your local machine by creating a new user account using the following email address and password combination:

```
email address: whiteHatHacker@
password: 123456
```

You should document your findings for the vulnerability report based on this scenario. Did the web site allow you to create this account? If so, you should make the appropriate recommendation to the development team and they should fix the problem.



### Scenario 2:
The CSO(Chief Security Officer) has been asking her development team to fix a problem with weak passwords for several months. The team continues to tell her that the problem has been fixed and there is nothing to be concened about. The CSO has reservations due to the team's past track record. So, she comes directly to you and your team in diplomatic tone and asks you to check behind the team to ensure they did not miss anything.

The CSO puts you in contact with their lead database administrator(a.k.a. DBA) for him to supply you with any information you need for your intelligence operation.

The DBA provides you with the following scripts that should be executed in your Juice-Shop docker container.

```
install sqlite
```

and

```json
sqlite3 /juice-shop/data/juiceshop.sqlite "SELECT id, email, password FROM Users;"
```

You notice the sql query returns some sensitive information---specifically the user's full credentials(e.g. email and password). You know that encrypting or hashing a password is a good practice and you see this in the console/terminal results.

Your team reviews your findings and they question you on how you are going to achieve the CSO's request since the passwords use an MD5 hashing algorithm.

A helpful colleague speaks up to relieve the pressure of the question that was just asked to you and says---```"I have way to find out! Why don't we use crackstation to see if there are known crackable passwords, so this way we can show some value to the CSO for our efforts."```

So, you ask your teammate to run-with-it and see what he can find. Your teammate comes back to you in a few hours and says he cannnot continue due to an emerging crisis in the NOC(Network Operations Center) and they need his immeidate attention. So, he asks you to pick up his workload.
 
You should take the MD5 hashed passwords from the query executed earlier and copy 20 of the passwords and use [CrackStation's Web Site](https://crackstation.net/) to determine the results.

Once done, you should add your findings to the vulnerability assessment report.


### Scenario 3:
You are sitting quietly at your desk and a teammate says quite loudly---`OMG! Here comes Ralph again!`.

Ralph storms into your team's working area and begins ranting about your team making him look bad to the CSO and other C-Level Executives at ACME Corp. You calmly and with your best diplomatic tone ask him to explain.

Ralph claims that yet another vulnerability has been found and this time it's in the login page of the web site. You ask---`Ralph, do you have any specific details on the vulnerability?`. He yells WTF! That's your job, you should be finding these problems,not me!!

After this heated exchange, your team spends a few hours on their investigation and comes back to you with the following statement: `We found this problem two months ago and provided Ralph a vulnerability report and let him know, that immediate remediation was needed. It seems no action was taken!`

To confirm your teams findings, you go the [Juice-Shop](http://localhost:3000/#/login) web site on your local machine and type the following SQL Injection into the email field with a fake password of any length:

`
' OR 1=1--
`

What did you find? Who are you now logged in "as"?

You should document your findings a second time for Ralph in your vulnerability report and provide details on your findings for them to fix. You should also consider how to provide this feedback to the CSO. Do you call a meeting and blame Ralph? Do you tell only Ralph or do you provide written documentation and communicate this to both Ralph and the CSO in a diplomatic fashion? At this point, no matter what you say-or-do, Ralph's reputation is on the line, so do you help him even though his behavior is likely going to continue?

###