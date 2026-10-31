## Quiz 1: Complete All Tasks Listed Below:

### Context:
This is your first quiz. It is a hands on test based on key topics that you have covered up to this point. This is an open/notes quiz, so you may use previous labs that you have completed to assist you. You have until the specified deadline noted in Canvas to have this completed.

### Task 1: Performing Docker Basics
- You should start the docker containers in the `week 5` directory using the VS Code terminal.
- You should list the running docker containers using the command line in VS Code.
- You should launch the `juice-shop` web site on your local machine using the correct port in the URL.
- You should record a 1-2 minute video showing me that you can accomplish these tasks and upload yoru video to Canvas.

### Task 2: Perform a Reconnaissance Mission
- Write a simple python program that issues an HTTP GET request to the following URL: `http://localhost:3000/rest/admin/application-version` and print the version of the application.
- Write a simple python program that issues an HTTP GET request to the following URL: `http://localhost:3000/rest/basket/1` and print the result to the console.
- Write a simple python program that issues an HTTP GET request to the following URL: `http://localhost:3000/api/Quantitys/1`and print the result to the console.
- Write a vulnerability report on your findings and upload it to Canvas
- Record a 2-3 minute video of this mission explaining each step and upload it to Canvas.


### Task 3: Executing Commands on a Docker Container
- You should use the VS Code extension `Dev Containers` and connect to the running `redis-cache-server` docker container and execute the following command on the VS Code terminal: `redis-cli`. 
- You should remain on the `redis-cache-server` container in VS Code and execute the following command: `redis-cli CONFIG GET *`. You should find the `dir` key in the list of data returned and its associated value and note this for the video.
- Once you are satisfied with your results, you can exit the `redis-cache-server` VS Code instance at this point.
- You should execute the proper command in VS Code terminal to shutdown all Docker containers that are currently running.
- Record a 2-3 minute video showing me that you can successfully execute these commands and upload it to Canvas.




