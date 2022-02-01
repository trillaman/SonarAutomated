# StaticScanning Wrapper

***

This one is for automated using SonarQube Scanner - currently "working" for wordpress plugin page It's still require
fixes for fully working and some improvements like watchdog for uploaded files and auto scanning them, but it works as
alpha version

### What's under the hood

Currently it's based on:

* Python with modules like requests, beautiful soup
* Docker on Linux VM - slashes for directory not changing on system like Windows (todo)
* os functions like curl, unzip and grep - so it's mostly designed for linux systems for now

### How to use

1. Create .env file with following fields:

   	SONNAR_URL=(PASTE HERE ADDRESS TO SONAR SCANNER with port :9000)
   	SONNAR_LOGIN=your sonar token here
   	SUDO_PASS=root user pass on linux

2. Start Docker backend with instructions from sonar page and then use command like:
   sudo docker-compose up

3. Run python script It's important to create docker volumes earlier to make data persistent after stopping docker
   container. Results will be visible after starting as well as login to sonar panel dashboard wil work This project is
   still under extending as well as fixing current bugs so please don't be mad if something will not work "just like
   that". Instead of this let me know what I can fix/add as functionality. Thanks!


      python3 main.py --file example.php -S S --name example