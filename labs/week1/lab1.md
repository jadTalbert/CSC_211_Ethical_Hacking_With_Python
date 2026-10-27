# Week 1 Lab 1: Set up & Configuration

### Step 1: Installing Python3 & VS Code
- [Download & Install Python](https://www.python.org/downloads/) (Windows, Linux & Mac OS)

- [Download & Install VS Code](https://code.visualstudio.com/download) (Windows, Linux & Mac OS)

### Step 2: Confirm Your Setup
- Open VS Code and confirm python3 is properly installed on your device. Watch the Instructor's video on how to do this! <<<< VIDEO LINK GOES HERE>>>>

### Step 3: Verify Git is Installed
- Open up a command prompt(Windows) or Terminal(Mac OS & Linux)
- Type in `git version` and hit the `Enter` key.
- If Git is installed you will see something like this and you should move to the next step:
    ```
    git version
    git version 2.50.1 (Apple Git-155)
    ```
- If Git is NOT installed you will receive an error message and you should [Install Git](https://git-scm.com/install/) for your Operating System(Windows,Linux,Mac OS)
- After you install Git, open the command line or terminal and type in `git version` again. If it is properly installed you will see the previously displayed message.

### Step 4: Download Docker Desktop
   ##### Note: (This works for Mac OS,Linux and Windows)
- <strong style="color:green">Note: </strong> Docker Desktop is a one-click-install application for Mac, Windows, and Linux that lets you build, share, and run containerized applications and microservices using a visual graphical user interface (GUI)

- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) - This is free! You Do <strong style="color:red">NOT</strong> pay for any products in this course.
- Install Docker Desktop on your local machine. Note, this may take a while depending on your specific device.
- After installation, make sure Docker Desktop is running by opening a command prompt or terminal and typing in the following command:
```docker ps```. You should see something like this:

    ```docker ps
        CONTAINER ID   IMAGE                            COMMAND                  CREATED        STATUS        PORTS                                         NAMES
    ```


### Step 5:
- Pull the juice-shop docker image by opening a command prompt(Windows) or Terminal(Mac OS) and typing in the following:
    `docker pull bkimminich/juice-shop:snapshot`. Wait for the image to completely download before moving to the next step.
- Start the juice-shop Docker image by typing the following into your command prompt or terminal.
    `docker run -d --name juice-shop -p 8080:3000 bkimminich/juice-shop:snapshot`
- Confirm the juice-shop Docker image is up-and-running by typing in the following:
    `docker ps`. You should see something like this:


     ``` docker ps
    CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                         NAMES
        a2c2e4012461   bkimminich/juice-shop   "/nodejs/bin/node /j…"   9 minutes ago   Up 9 minutes   0.0.0.0:8080->3000/tcp, [::]:8080->3000/tcp   juice-shop```

- Next, in the command prompt or terminal, type in the following `docker debug juice-shop`. This is the interactive debugger, which allows us to gain access the Docker image file system. This make take a few minutes as the image downloads--just wait it to complete when done, you will see something like this:

    ```docker debug juice-shop

        Builtin commands:
        - install [tool1] [tool2] ...    Add Nix packages from: https://search.nixos.org/packages
        - uninstall [tool1] [tool2] ...  Uninstall NixOS package(s).
        - entrypoint                     Print/lint/run the entrypoint.
        - builtins                       Show builtin commands.

        Checks:
        ✓ distro:            Distroless
        ✓ entrypoint linter: no errors (run 'entrypoint' for details)

        This is an attach shell, i.e.:
        - Any changes to the container filesystem are visible to the container directly.
        - The /nix directory is invisible to the actual container.
                                                                                                                                                                        Version: 0.0.47
        root@a2c2e4012461 /juice-shop [juice-shop]
    docker >```

    
### Step 6:
- Confirm the Web Site installed on this container is working by opening a browser(e.g. Chrome) and go to `http://localhost:8080`. 
- If the web site loads, you have successfully installed the application for docker. If it is not running, then you should go back and review these instructions more closely and try it again.

#### Note: 
If you made a mistake, it's no big deal and this is the beauty with Docker. You can simply start over. So, if things are not going well, simply remove the container by typing `docker rm -f juice-shop` into the command prompt or terminal. This will remove the container and you can start over from the beginning.

### Step 7
- If you have not already cloned this repository to your local machine, you should do it now using VS Code.

### How To submit this lab
- You should record a 1-2 minute video showing me that you can execute the following commands with working docker containers
    - using Windows command line or Mac OS Terminal execute `docker ps`
    - launch VS Code and show me that it is installed
    - using VS Code, open the terminal and execute `python3 --version`
    - using VS Code, open the terminal and execute `git version`
    





